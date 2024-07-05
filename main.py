import tkinter as tk
from tkinter import messagebox
import time


questions = [
    {"question": "What is the capital of France?", "options": ["Paris", "London", "Rome", "Berlin"], "answer": "Paris", "difficulty": "easy"},
    {"question": "What is the largest planet in our solar system?", "options": ["Earth", "Mars", "Jupiter", "Saturn"], "answer": "Jupiter", "difficulty": "easy"},
    {"question": "Who wrote 'Hamlet'?", "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Jane Austen"], "answer": "William Shakespeare", "difficulty": "medium"},
    {"question": "What is the square root of 64?", "options": ["6", "7", "8", "9"], "answer": "8", "difficulty": "easy"},
    {"question": "What is the chemical symbol for gold?", "options": ["Au", "Ag", "Fe", "Hg"], "answer": "Au", "difficulty": "medium"},
    {"question": "In which year did the Titanic sink?", "options": ["1912", "1905", "1920", "1918"], "answer": "1912", "difficulty": "hard"},
    {"question": "Who discovered penicillin?", "options": ["Alexander Fleming", "Marie Curie", "Isaac Newton", "Albert Einstein"], "answer": "Alexander Fleming", "difficulty": "hard"},
]

class TriviaQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Trivia Quiz Game")

        self.score = 0
        self.question_index = 0
        self.selected_difficulty = "easy"
        self.time_limit = 10 
        self.timer_id = None

        
        self.start_frame = tk.Frame(root)
        self.start_frame.pack(pady=20)
        tk.Label(self.start_frame, text="Select Difficulty Level:", font=("Arial", 16)).pack(pady=10)

        self.difficulty_var = tk.StringVar(value="easy")
        difficulties = ["easy", "medium", "hard"]
        for difficulty in difficulties:
            tk.Radiobutton(self.start_frame, text=difficulty.capitalize(), variable=self.difficulty_var, value=difficulty, font=("Arial", 14)).pack(anchor=tk.W)

        tk.Button(self.start_frame, text="Start Quiz", font=("Arial", 14), command=self.start_quiz).pack(pady=20)

        
        self.quiz_frame = tk.Frame(root)

        self.question_label = tk.Label(self.quiz_frame, text="", font=("Arial", 16), wraplength=400, justify="center")
        self.question_label.pack(pady=20)

        self.option_buttons = []
        for _ in range(4):
            button = tk.Button(self.quiz_frame, text="", font=("Arial", 14), width=20, command=lambda i=_: self.check_answer(i))
            button.pack(pady=5)
            self.option_buttons.append(button)

        self.score_label = tk.Label(self.quiz_frame, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(pady=20)

        self.timer_label = tk.Label(self.quiz_frame, text=f"Time left: {self.time_limit} seconds", font=("Arial", 14))
        self.timer_label.pack(pady=10)

        self.next_button = tk.Button(self.quiz_frame, text="Next", font=("Arial", 14), state="disabled", command=self.next_question)
        self.next_button.pack(pady=10)

    def start_quiz(self):
        self.selected_difficulty = self.difficulty_var.get()
        self.start_frame.pack_forget()
        self.quiz_frame.pack(pady=20)
        self.load_question()

    def load_question(self):
        if self.question_index < len(questions):
            filtered_questions = [q for q in questions if q["difficulty"] == self.selected_difficulty]
            if self.question_index < len(filtered_questions):
                question_data = filtered_questions[self.question_index]
                self.question_label.config(text=question_data["question"])
                for i, option in enumerate(question_data["options"]):
                    self.option_buttons[i].config(text=option)
                self.reset_timer()
                self.start_timer()
            else:
                self.end_quiz()
        else:
            self.end_quiz()

    def reset_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.time_left = self.time_limit
        self.timer_label.config(text=f"Time left: {self.time_left} seconds")

    def start_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.start_timer)
        else:
            self.check_answer(None)

    def check_answer(self, index):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        filtered_questions = [q for q in questions if q["difficulty"] == self.selected_difficulty]
        question_data = filtered_questions[self.question_index]

        if index is not None:
            selected_answer = self.option_buttons[index].cget("text")
            if selected_answer == question_data["answer"]:
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                messagebox.showinfo("Correct!", "That's the right answer!")
            else:
                messagebox.showinfo("Incorrect", f"Sorry, the correct answer was: {question_data['answer']}")
        else:
            messagebox.showinfo("Time's up!", f"Sorry, the correct answer was: {question_data['answer']}")

        self.next_button.config(state="normal")

    def next_question(self):
        self.question_index += 1
        self.next_button.config(state="disabled")
        self.load_question()

    def end_quiz(self):
        messagebox.showinfo("Quiz Over", f"Your final score is: {self.score}")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaQuiz(root)
    root.mainloop()
