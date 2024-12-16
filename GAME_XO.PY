import tkinter as tk  #  (GUI) مكتبة  الواجهة الرسومية
import random  # مكتبة لتوليد حركات الحاسوب العشوائية

#  النافذة الرئيسية
window = tk.Tk()
window.title("Tic Tac Toe")
window.geometry("400x500")

# المتغيرات الأساسية
player_score = 0
computer_score = 0
ties = 0
current_player = "X"
buttons = []

# تحديث النتيجة  
def update_score_label():
    score_label.config(
        text=f"You : {player_score}  |  Computer : {computer_score}"
    )

# التحقق من  الفائز أو المتعادل
def check_winner():
    global player_score, computer_score, ties
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # الصفوف
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # الأعمدة
        [0, 4, 8], [2, 4, 6]              # الأقطار
    ]

    for set in winning_combinations:
        if (
            buttons[set[0]]["text"] == buttons[set[1]]["text"] == 
            buttons[set[2]]["text"] and buttons[set[0]]["text"] != ""
        ):
            for index in set:
                buttons[index].config(bg="cyan")
            if buttons[set[0]]["text"] == "X":
                result_label.config(text="X Wins !" , fg="cyan"  )
                player_score += 1
            else:
                result_label.config(text="O Wins !" , fg="cyan")
                computer_score += 1
            update_score_label()
            disable_buttons()
            return True

    # في حالة التعادل
    if all(button["text"] != "" for button in buttons):
        for button in buttons:
            button.config(bg="red")
        result_label.config(text="Tie! , No Winner !" , fg="red")
        ties += 1
        update_score_label()
        return True

    return False

# تعطيل جميع الأزرار بعد انتهاء الجولة
def disable_buttons():
    for button in buttons:
        button.config(state="disabled")

# إعادة تشغيل اللعبة
def restart_game():
    global current_player
    current_player = "X"
    result_label.config(text="")
    for button in buttons:
        button.config(text="", state="normal" , bg="SystemButtonFace")

def make_move(self, row, col):
        if self.board[row][col] == "" and not self.check_game_over():
            self.board[row][col] = self.current_player
            self.update_buttons_state()
            if self.check_game_over():
                self.update_score_label()
                self.show_result_message()
            else:
                self.switch_player()
                self.computer_move()
# حركة الحاسوب
def computer_move():
    available_buttons = [button for button in buttons if button["text"] == ""]
    if available_buttons:
        chosen_button = random.choice(available_buttons)
        chosen_button.config(text="O")
        if not check_winner():
            global current_player
            current_player = "X"

# حدث عند الضغط على زر
def button_click(index):
    global current_player
    if buttons[index]["text"] == "" and current_player == "X":
        buttons[index].config(text="X")
        if not check_winner():
            current_player = "O"
            window.after(300, computer_move )  # delay for computer
            
# تصميم واجهة المستخدم
score_label = tk.Label(window, text="X : 0 | O : 0 ", font=("Arial", 14))
score_label.pack(pady=10 )

result_label = tk.Label(window, text="", font=("Arial", 16))
result_label.pack(pady=10 )

frame = tk.Frame(window)
frame.pack( )

# إنشاء شبكة الأزرار 3x3
for i in range(3):
    for j in range(3):
        button = tk.Button(
            frame, text="", font=("Arial", 20), width=5, height=2,
            command=lambda index=len(buttons): button_click(index)
        )
        button.grid(row=i, column=j)
        buttons.append(button )

restart_button = tk.Button(window, text="Restart", font=("Arial", 14), command=restart_game)
restart_button.pack(pady=20)


# تشغيل التطبيق
update_score_label()
window.mainloop()