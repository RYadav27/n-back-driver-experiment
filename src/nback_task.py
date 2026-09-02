import random
import threading
import time
import pythoncom
import win32com.client

from pynput import keyboard

from src.data_manager import (
    create_workbook,
    append_trial,
    save_workbook,
)


TOTAL_TRIALS = 20
INTERVAL = 2.25


class NBackRunner:

    def __init__(self, run_number=1, driver_number=1):

        self.run_number = run_number

        self.driver_number = driver_number

        self.total_trials = TOTAL_TRIALS

        self.completed_trials = 0

        self.match_count = 0

        self.no_match_count = 0

        self.skip_count = 0

        self.status = "ready"

        self.last_number = None

        self.error = ""

        self.output_path = None

        self._stop_event = threading.Event()

        self._response_event = threading.Event()

        self._response_lock = threading.Lock()

        self._current_response = None

        self._current_response_time = None

        self._thread = None


    # ========================================================
    # START
    # ========================================================

    def start(self):

        if self.status != "ready":
            return

        self.status = "running"

        self._thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self._thread.start()


    # ========================================================
    # MANUAL RESPONSE FROM STREAMLIT BUTTON
    # ========================================================

    def manual_response(self, response):

        response = response.upper()

        if response not in ("M", "N", "S"):
            return

        with self._response_lock:

            if self._current_response is None:

                self._current_response = response

                self._current_response_time = (
                    time.perf_counter()
                )

                self._response_event.set()


    # ========================================================
    # KEYBOARD RESPONSE
    # ========================================================

    def _key_press(self, key):

        try:

            value = key.char.upper()

        except AttributeError:

            return True


        if value in ("M", "N", "S"):

            with self._response_lock:

                if self._current_response is None:

                    self._current_response = value

                    self._current_response_time = (
                        time.perf_counter()
                    )

                    self._response_event.set()


        return True


    # ========================================================
    # RUN EXPERIMENT
    # ========================================================

    def _run(self):

        pythoncom.CoInitialize()

        speaker = None

        wb = None

        try:

            # ------------------------------------------------
            # CREATE EXCEL
            # ------------------------------------------------

            wb, ws, path = create_workbook(
                run_number=self.run_number,
                driver_number=self.driver_number
            )

            self.output_path = path


            # ------------------------------------------------
            # WINDOWS SPEECH
            # ------------------------------------------------

            speaker = win32com.client.Dispatch(
                "SAPI.SpVoice"
            )


            # ------------------------------------------------
            # KEYBOARD LISTENER
            # ------------------------------------------------

            listener = keyboard.Listener(
                on_press=self._key_press
            )

            listener.start()


            # ------------------------------------------------
            # PRECISE STIMULUS-ONSET TIMING
            # ------------------------------------------------

            next_onset = time.perf_counter()


            for trial in range(
                1,
                TOTAL_TRIALS + 1
            ):

                if self._stop_event.is_set():
                    break


                # --------------------------------------------
                # WAIT FOR NEXT STIMULUS ONSET
                # --------------------------------------------

                wait_time = (
                    next_onset -
                    time.perf_counter()
                )

                if wait_time > 0:

                    time.sleep(wait_time)


                # --------------------------------------------
                # GENERATE NUMBER
                # --------------------------------------------

                number = random.randint(
                    1,
                    9
                )

                self.last_number = number


                # --------------------------------------------
                # RESET RESPONSE
                # --------------------------------------------

                with self._response_lock:

                    self._current_response = None

                    self._current_response_time = None


                self._response_event.clear()


                # --------------------------------------------
                # STIMULUS ONSET
                # --------------------------------------------

                stimulus_onset = time.perf_counter()


                # Speak asynchronously.
                # The number audio is the only audio output.

                speaker.Speak(
                    str(number),
                    1
                )


                # --------------------------------------------
                # WAIT FOR OBSERVER RESPONSE
                # --------------------------------------------

                # The observer can press M/N/S at any
                # point during the trial interval.

                self._response_event.wait(
                    timeout=INTERVAL
                )


                # --------------------------------------------
                # READ RESPONSE
                # --------------------------------------------

                with self._response_lock:

                    response = self._current_response

                    response_time = (
                        self._current_response_time
                    )


                # If no key was pressed,
                # save blank response.

                if response is None:

                    response = ""

                    reaction_time_ms = ""

                else:

                    reaction_time_ms = round(
                        (
                            response_time -
                            stimulus_onset
                        ) * 1000,
                        2
                    )


                # --------------------------------------------
                # UPDATE COUNTS
                # --------------------------------------------

                if response == "M":

                    self.match_count += 1

                elif response == "N":

                    self.no_match_count += 1

                elif response == "S":

                    self.skip_count += 1


                # --------------------------------------------
                # SAVE TRIAL
                # --------------------------------------------

                append_trial(
                    ws,
                    trial,
                    number,
                    response,
                    reaction_time_ms
                )


                # Save continuously
                save_workbook(
                    wb,
                    path
                )


                # --------------------------------------------
                # UPDATE PROGRESS
                # --------------------------------------------

                self.completed_trials = trial


                # --------------------------------------------
                # NEXT STIMULUS
                # --------------------------------------------

                next_onset += INTERVAL


            # ------------------------------------------------
            # STOP LISTENER
            # ------------------------------------------------

            listener.stop()

            listener.join()


            # ------------------------------------------------
            # FINAL SAVE
            # ------------------------------------------------

            save_workbook(
                wb,
                path
            )


            if self._stop_event.is_set():

                self.status = "stopped"

            else:

                self.status = "completed"


        except Exception as exc:

            self.error = (
                f"{type(exc).__name__}: {exc}"
            )

            self.status = "error"


        finally:

            try:

                if speaker is not None:

                    speaker.Speak(
                        "",
                        2
                    )

            except Exception:
                pass


            pythoncom.CoUninitialize()


    # ========================================================
    # STOP
    # ========================================================

    def stop(self):

        self._stop_event.set()

        self._response_event.set()
        
