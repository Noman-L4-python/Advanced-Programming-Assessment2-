import tkinter as tk
from tkinter import messagebox
import requests
import random
import html

class Quiz:
    def __init__(self, root):
        self.root = root
        self.difficulty = ""
        self.num_questions = 10
        self.questions = []
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        self.root.config(bg="#6c5ce7")
        self.font = ("Segoe UI", 18)
        self.button_font = ("Segoe UI", 16, "bold")
        self.setup()

    def setup(self):
        self.clear()
        main_frame = tk.Frame(self.root, bg="#6c5ce7", width=900, height=600)
        main_frame.place(relwidth=1, relheight=1)
        title_label = tk.Label(main_frame, text="Quizzee", font=("Segoe UI", 50, "bold"), fg="white", bg="#6c5ce7")
        title_label.pack(pady=50)
        tk.Label(main_frame, text="Select Difficulty", font=self.font, fg="white", bg="#6c5ce7").pack(pady=10)
        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("easy")
        difficulty_dropdown = tk.OptionMenu(main_frame, self.difficulty_var, "easy", "medium", "hard")
        difficulty_dropdown.config(font=self.font, width=20, bg="#1e90ff", fg="white", relief="flat")
        difficulty_dropdown.pack(pady=10)
        tk.Label(main_frame, text="Select Number of Questions", font=self.font, fg="white", bg="#6c5ce7").pack(pady=10)
        self.num_questions_var = tk.StringVar()
        self.num_questions_var.set("10")
        num_questions_dropdown = tk.OptionMenu(main_frame, self.num_questions_var, "9", "10", "12")
        num_questions_dropdown.config(font=self.font, width=20, bg="#1e90ff", fg="white", relief="flat")
        num_questions_dropdown.pack(pady=10)
        start_button = tk.Button(main_frame, text="Start Quiz", font=self.button_font, command=self.start, bg="#ff4757", fg="white", relief="flat", width=20, height=2)
        start_button.pack(pady=30)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def fetch(self):
        difficulty_level = self.difficulty
        num_questions = int(self.num_questions)
        print(f"Fetching questions with: Difficulty = {difficulty_level}, Number of Questions = {num_questions}")
        url = f"https://opentdb.com/api.php?amount={num_questions}&difficulty={difficulty_level}&type=boolean"
        try:
            response = requests.get(url)
            data = response.json()
            print("API Response:", data)
            if data['response_code'] == 0 and data['results']:
                self.questions = data['results']
            else:
                self.questions = []
                print(f"API Error: {data['response_code']} - No questions available for the given parameters.")
                messagebox.showerror("Error", f"No questions available for the selected difficulty '{self.difficulty}'. Please try different options.")
                self.retry()
        except Exception as e:
            self.questions = []
            print(f"An error occurred while fetching questions: {e}")
            messagebox.showerror("Error", f"An error occurred while fetching questions: {e}")

    def retry(self):
        self.difficulty = "easy"
        self.num_questions = "9"
        print(f"Retrying fetch with: Difficulty = easy, Number of Questions = 9")
        self.fetch()

    def start(self):
        self.difficulty = self.difficulty_var.get()
        self.num_questions = self.num_questions_var.get()
        if self.difficulty and self.num_questions:
            self.fetch()
            if self.questions:
                self.current_question = 0
                self.score = 0
                self.display()
            else:
                tk.Label(self.root, text="No questions found or error fetching questions. Please check your inputs.", font=self.font, fg="red", bg="#6c5ce7").pack()
        else:
            messagebox.showerror("Error", "Please select all options before starting the quiz!")

    def display(self):
        self.clear()
        question = self.questions[self.current_question]
        question_text = html.unescape(question['question'])
        quiz_frame = tk.Frame(self.root, bg="#6c5ce7", width=900, height=600)
        quiz_frame.place(relwidth=1, relheight=1)
        question_widget = tk.Label(quiz_frame, text=question_text, font=("Segoe UI", 24), fg="white", bg="#6c5ce7", wraplength=750, justify="center")
        question_widget.pack(pady=30)
        options = ["True", "False"]
        self.option_buttons = []
        button_frame = tk.Frame(quiz_frame, bg="#6c5ce7")
        button_frame.pack(pady=20)
        for option in options:
            button = tk.Button(button_frame, text=option, font=("Segoe UI", 14), command=lambda ans=option: self.check(ans), bg="#1e90ff", fg="white", relief="flat", width=12, height=1)
            button.pack(side=tk.LEFT, padx=20)
            self.option_buttons.append(button)
        progress_text = f"Question {self.current_question + 1} of {self.num_questions}"
        progress_label = tk.Label(quiz_frame, text=progress_text, font=("Segoe UI", 16), fg="white", bg="#6c5ce7")
        progress_label.pack(pady=10)

    def check(self, answer):
        correct_answer = "True" if self.questions[self.current_question]['correct_answer'] else "False"
        for button in self.option_buttons:
            button.config(state=tk.DISABLED)
        if answer == correct_answer:
            self.score += 1
            feedback_text = "Correct!"
            feedback_color = "#2ecc71"
        else:
            feedback_text = f"Incorrect! The correct answer is: {correct_answer}"
            feedback_color = "#e74c3c"
        feedback_label = tk.Label(self.root, text=feedback_text, font=("Segoe UI", 22, "bold"), fg=feedback_color, bg="#6c5ce7")
        feedback_label.pack(pady=20)
        self.root.after(1500, self.next)

    def next(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.display()
        else:
            self.results()

    def results(self):
        self.clear()
        result_frame = tk.Frame(self.root, bg="#6c5ce7", width=900, height=600)
        result_frame.place(relwidth=1, relheight=1)
        tk.Label(result_frame, text=f"Your final score: {self.score}/{self.num_questions}", font=("Segoe UI", 30, "bold"), fg="white", bg="#6c5ce7").pack(pady=30)
        restart_button = tk.Button(result_frame, text="Start Over", font=self.button_font, command=self.setup, bg="#2ecc71", fg="white", relief="flat", width=20, height=2)
        restart_button.pack(pady=30)

root = tk.Tk()
quiz = Quiz(root)
root.mainloop()
