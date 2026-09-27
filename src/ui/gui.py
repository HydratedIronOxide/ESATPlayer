import tkinter as tk

from src.qa_manager.result_generator import mark_set
from src.paths import BANK_DIR
from src.qa_manager.question_loader import load_questions
from src.test_driver.test_player import TestPlayer



class BankBrowser(tk.Toplevel):
    """Used to select the question deck from the bank directory"""
    def __init__(self, parent, callback):
        super().__init__(parent)
        self._callback = callback
        self._bank_listbox = tk.Listbox(self, font=("Arial", 16))
        self._bank_listbox.pack(fill="both", expand=True)
        self._bank_listbox.bind("<Double-Button-1>", self.__on_select)

        self.__populate_bank_list()

    def __populate_bank_list(self):
        self._bank_listbox.delete(0, tk.END)
        for bank_file in BANK_DIR.glob("*.json"):
            self._bank_listbox.insert(tk.END, bank_file.name)

    def __on_select(self, event):
        selection = self._bank_listbox.curselection()
        if selection:
            bank_file = self._bank_listbox.get(selection[0])
            self._callback(bank_file)
            self.destroy()


class TestResultViewer(tk.Toplevel):
    """Used to view the results of a test"""
    def __init__(self, parent, results):
        super().__init__(parent)
        self.title("Test Results")
        self.geometry("800x600")

        self._results = results

        self._result_listbox = tk.Listbox(self, font=("Arial", 16))
        self._result_listbox.pack(fill="both", expand=True)

        self.__populate_result_list()

    def __populate_result_list(self):
        self._result_listbox.delete(0, tk.END)
        for result in self._results:
            qid = result['qid']
            selected = result['selected']
            correct = result['correct']
            time = result['time']
            is_correct = result['is_correct']
            self._result_listbox.insert(tk.END, f"QID: {qid} | Selected: {selected} | Correct: {correct} | Time: {time}s | {'Correct' if is_correct else 'Incorrect'}")





class App:
    def __init__(self):
        self._tk = tk.Tk()
        self._tk.title("ESAT Player")

        self._test_running = False

        self._load_button = tk.Button(self._tk, text="Load Question Bank", command=self.__open_bank_browser, font=("Arial", 16))
        self._load_button.pack(padx=20, pady=20)

        self._tk.mainloop()

    def __open_bank_browser(self):
        if not self._test_running:
            BankBrowser(self._tk, self.__on_bank_selected)

    def __on_bank_selected(self, bank_file):
        print(f"Selected bank: {bank_file}")
        q = load_questions(bank_file)  # Load the questions from the selected bank
        TestPlayer(self._tk, q["questions"], q['name'], self.__finish_callback)  # Open the TestPlayer with the loaded questions
        self._test_running = True

    def __finish_callback(self, test_data, question_data):
        print("Test finished.")
        self._test_running = False

        res = mark_set(test_data, question_data)  # Mark the test data against the question data
        TestResultViewer(self._tk, res)  # Open the TestResultViewer with the results










