import streamlit as st
import random
import json
import time

# Set page configuration
st.set_page_config(
    page_title="Kids Learning Adventure",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for colorful, child-friendly interface
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .game-title {
        font-size: 2rem;
        color: #4ECDC4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .game-container {
        background-color: #F8F9FA;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .btn-primary {
        background-color: #FF9F1C;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 1.2rem;
        cursor: pointer;
        margin: 5px;
        transition: all 0.3s ease;
    }
    .btn-primary:hover {
        background-color: #FF8C00;
        transform: scale(1.05);
    }
    .btn-secondary {
        background-color: #8EE4AF;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 1.2rem;
        cursor: pointer;
        margin: 5px;
        transition: all 0.3s ease;
    }
    .btn-secondary:hover {
        background-color: #5CDB95;
        transform: scale(1.05);
    }
    .mascot {
        font-size: 5rem;
        text-align: center;
        margin: 20px 0;
    }
    .message-bubble {
        background-color: white;
        border-radius: 20px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        position: relative;
    }
    .message-bubble:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        width: 0;
        height: 0;
        border: 20px solid transparent;
        border-top-color: white;
        border-bottom: 0;
        margin-left: -20px;
        margin-bottom: -20px;
    }
    .score-display {
        font-size: 1.5rem;
        font-weight: bold;
        color: #5D5D5D;
        text-align: right;
        margin: 10px 0;
    }
    .star {
        color: #FFD700;
        font-size: 2rem;
    }
    .canvas-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .color-palette {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        margin: 10px 0;
    }
    .color-btn {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin: 5px;
        border: 2px solid #ddd;
        cursor: pointer;
    }
    .brush-size-container {
        display: flex;
        justify-content: center;
        margin: 10px 0;
    }
    .brush-btn {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin: 5px;
        border: 2px solid #ddd;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
    }
    .shape-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        margin: 20px 0;
    }
    .shape {
        margin: 10px;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .shape:hover {
        transform: scale(1.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'current_game' not in st.session_state:
    st.session_state.current_game = None
if 'counting_score' not in st.session_state:
    st.session_state.counting_score = 0
if 'alphabet_score' not in st.session_state:
    st.session_state.alphabet_score = 0
if 'shapes_score' not in st.session_state:
    st.session_state.shapes_score = 0
if 'mascot_message' not in st.session_state:
    st.session_state.mascot_message = "Welcome! Choose an activity to start learning!"
if 'show_reward' not in st.session_state:
    st.session_state.show_reward = False

# Helper functions
def display_mascot(message=None):
    """Display the mascot with a message"""
    if message:
        st.session_state.mascot_message = message
    
    st.markdown(f"""
    <div class="mascot">🐻</div>
    <div class="message-bubble">
        <p>{st.session_state.mascot_message}</p>
    </div>
    """, unsafe_allow_html=True)

def display_score(score_type):
    """Display the score for a specific game"""
    if score_type == "counting":
        score = st.session_state.counting_score
    elif score_type == "alphabet":
        score = st.session_state.alphabet_score
    elif score_type == "shapes":
        score = st.session_state.shapes_score
    else:
        score = 0
    
    st.markdown(f"""
    <div class="score-display">
        Score: {score} {'<span class="star">⭐</span>' * (score // 5)}
    </div>
    """, unsafe_allow_html=True)

def back_to_menu():
    """Reset current game to return to menu"""
    st.session_state.current_game = None
    st.session_state.mascot_message = "Welcome back! Choose another activity!"

def counting_game():
    """Counting game implementation"""
    st.markdown('<h1 class="game-title">Counting Game</h1>', unsafe_allow_html=True)
    
    # Generate random objects to count
    if 'counting_objects' not in st.session_state or 'counting_question' not in st.session_state:
        count = random.randint(3, 10)
        shapes = ['circle', 'square', 'triangle', 'star']
        colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
        
        objects = []
        for _ in range(count):
            obj_shape = random.choice(shapes)
            obj_color = random.choice(colors)
            objects.append((obj_shape, obj_color))
        
        st.session_state.counting_objects = objects
        st.session_state.counting_answer = count
        st.session_state.counting_question = f"How many {random.choice(['shapes', 'circles', 'squares', 'triangles', 'stars'])} do you see?"
        st.session_state.counting_feedback = None
    
    # Display the question
    st.markdown(f'<h2>{st.session_state.counting_question}</h2>', unsafe_allow_html=True)
    
    # Display the objects
    cols = st.columns(5)
    for i, (shape, color) in enumerate(st.session_state.counting_objects):
        with cols[i % 5]:
            if shape == 'circle':
                st.markdown(f'<div style="width:100px;height:100px;background-color:{color};border-radius:50%;margin:10px auto;"></div>', unsafe_allow_html=True)
            elif shape == 'square':
                st.markdown(f'<div style="width:100px;height:100px;background-color:{color};margin:10px auto;"></div>', unsafe_allow_html=True)
            elif shape == 'triangle':
                st.markdown(f'<div style="width:0;height:0;border-left:50px solid transparent;border-right:50px solid transparent;border-bottom:100px solid {color};margin:10px auto;"></div>', unsafe_allow_html=True)
            elif shape == 'star':
                st.markdown(f'<div style="font-size:100px;color:{color};text-align:center;margin:10px auto;">⭐</div>', unsafe_allow_html=True)
    
    # Create answer options
    correct_answer = st.session_state.counting_answer
    wrong_options = [correct_answer - 1, correct_answer + 1, correct_answer + 2]
    wrong_options = [opt for opt in wrong_options if opt > 0 and opt != correct_answer]
    
    if len(wrong_options) < 3:
        wrong_options.extend([correct_answer - 2, correct_answer + 3, correct_answer - 3])
        wrong_options = [opt for opt in wrong_options if opt > 0 and opt != correct_answer]
    
    options = [correct_answer] + random.sample(wrong_options, min(3, len(wrong_options)))
    random.shuffle(options)
    
    # Display answer options
    cols = st.columns(len(options))
    for i, option in enumerate(cols):
        with option:
            if st.button(str(options[i]), key=f"counting_option_{i}"):
                if options[i] == correct_answer:
                    st.session_state.counting_score += 1
                    st.session_state.counting_feedback = "Correct! Great job! 🎉"
                    st.session_state.mascot_message = "You're doing great! Keep counting!"
                    # Generate new question
                    del st.session_state.counting_objects
                    del st.session_state.counting_question
                else:
                    st.session_state.counting_feedback = f"Not quite. Try again! The answer was {correct_answer}."
                    st.session_state.mascot_message = "Don't worry, you'll get it next time!"
                st.experimental_rerun()
    
    # Display feedback
    if st.session_state.counting_feedback:
        if "Correct" in st.session_state.counting_feedback:
            st.markdown(f'<div style="color:green;font-size:1.5rem;text-align:center;">{st.session_state.counting_feedback}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="color:red;font-size:1.5rem;text-align:center;">{st.session_state.counting_feedback}</div>', unsafe_allow_html=True)
    
    # Display score
    display_score("counting")
    
    # Back button
    if st.button("Back to Menu", key="counting_back"):
        back_to_menu()
        st.experimental_rerun()

def alphabet_game():
    """Alphabet learning game implementation"""
    st.markdown('<h1 class="game-title">Alphabet Learning</h1>', unsafe_allow_html=True)
    
    # Initialize current letter
    if 'current_letter' not in st.session_state:
        st.session_state.current_letter = 'A'
    
    # Word examples for each letter
    word_examples = {
        'A': 'Apple', 'B': 'Ball', 'C': 'Cat', 'D': 'Dog', 'E': 'Elephant',
        'F': 'Fish', 'G': 'Goat', 'H': 'Hat', 'I': 'Ice cream', 'J': 'Jump',
        'K': 'Kite', 'L': 'Lion', 'M': 'Moon', 'N': 'Nest', 'O': 'Orange',
        'P': 'Penguin', 'Q': 'Queen', 'R': 'Rainbow', 'S': 'Sun', 'T': 'Tree',
        'U': 'Umbrella', 'V': 'Violin', 'W': 'Water', 'X': 'Xylophone', 'Y': 'Yacht', 'Z': 'Zebra'
    }
    
    # Display the current letter
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    letter_color = random.choice(colors)
    
    st.markdown(f'<div style="font-size:10rem;color:{letter_color};text-align:center;font-weight:bold;">{st.session_state.current_letter}</div>', unsafe_allow_html=True)
    
    # Show word example if requested
    if 'show_word' in st.session_state and st.session_state.show_word:
        word = word_examples.get(st.session_state.current_letter, '')
        st.markdown(f'<div style="font-size:2rem;text-align:center;">{word}</div>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Previous", key="alphabet_prev"):
            if st.session_state.current_letter == 'A':
                st.session_state.current_letter = 'Z'
            else:
                st.session_state.current_letter = chr(ord(st.session_state.current_letter) - 1)
            st.session_state.show_word = False
            st.experimental_rerun()
    
    with col2:
        if st.button("Show Word", key="alphabet_word"):
            st.session_state.show_word = True
            st.session_state.alphabet_score += 1
            st.session_state.mascot_message = f"Great job learning the letter {st.session_state.current_letter}!"
            st.experimental_rerun()
    
    with col3:
        if st.button("Next", key="alphabet_next"):
            if st.session_state.current_letter == 'Z':
                st.session_state.current_letter = 'A'
            else:
                st.session_state.current_letter = chr(ord(st.session_state.current_letter) + 1)
            st.session_state.show_word = False
            st.experimental_rerun()
    
    # Display score
    display_score("alphabet")
    
    # Back button
    if st.button("Back to Menu", key="alphabet_back"):
        back_to_menu()
        st.experimental_rerun()

def drawing_game():
    """Drawing canvas implementation using HTML5 Canvas"""
    st.markdown('<h1 class="game-title">Drawing Canvas</h1>', unsafe_allow_html=True)
    
    # Instructions
    st.markdown('<div style="font-size:1.2rem;text-align:center;margin-bottom:20px;">Click and drag to draw. Select colors and brush sizes below.</div>', unsafe_allow_html=True)
    
    # HTML5 Canvas for drawing
    drawing_code = """
    <div class="canvas-container">
        <canvas id="drawingCanvas" width="800" height="400" style="border:2px solid #ddd;border-radius:10px;"></canvas>
    </div>
    
    <div class="color-palette">
        <div class="color-btn" style="background-color:black;" onclick="changeColor('black')"></div>
        <div class="color-btn" style="background-color:red;" onclick="changeColor('red')"></div>
        <div class="color-btn" style="background-color:green;" onclick="changeColor('green')"></div>
        <div class="color-btn" style="background-color:blue;" onclick="changeColor('blue')"></div>
        <div class="color-btn" style="background-color:yellow;" onclick="changeColor('yellow')"></div>
        <div class="color-btn" style="background-color:purple;" onclick="changeColor('purple')"></div>
        <div class="color-btn" style="background-color:orange;" onclick="changeColor('orange')"></div>
        <div class="color-btn" style="background-color:pink;" onclick="changeColor('pink')"></div>
        <div class="color-btn" style="background-color:brown;" onclick="changeColor('brown')"></div>
        <div class="color-btn" style="background-color:white;" onclick="changeColor('white')"></div>
    </div>
    
    <div class="brush-size-container">
        <div class="brush-btn" onclick="changeBrushSize(2)"><div style="width:2px;height:2px;background-color:black;border-radius:50%;"></div></div>
        <div class="brush-btn" onclick="changeBrushSize(5)"><div style="width:5px;height:5px;background-color:black;border-radius:50%;"></div></div>
        <div class="brush-btn" onclick="changeBrushSize(10)"><div style="width:10px;height:10px;background-color:black;border-radius:50%;"></div></div>
        <div class="brush-btn" onclick="changeBrushSize(15)"><div style="width:15px;height:15px;background-color:black;border-radius:50%;"></div></div>
        <div class="brush-btn" onclick="changeBrushSize(20)"><div style="width:20px;height:20px;background-color:black;border-radius:50%;"></div></div>
    </div>
    
    <div style="text-align:center;margin-top:20px;">
        <button class="btn-primary" onclick="clearCanvas()">Clear Canvas</button>
    </div>
    
    <script>
        const canvas = document.getElementById('drawingCanvas');
        const ctx = canvas.getContext('2d');
        
        // Set canvas background
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        let isDrawing = false;
        let currentColor = 'black';
        let currentSize = 5;
        
        canvas.addEventListener('mousedown', startDrawing);
        canvas.addEventListener('mousemove', draw);
        canvas.addEventListener('mouseup', stopDrawing);
        canvas.addEventListener('mouseout', stopDrawing);
        
        function startDrawing(e) {
            isDrawing = true;
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            ctx.beginPath();
            ctx.moveTo(x, y);
        }
        
        function draw(e) {
            if (!isDrawing) return;
            
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            ctx.lineWidth = currentSize;
            ctx.lineCap = 'round';
            ctx.strokeStyle = currentColor;
            
            ctx.lineTo(x, y);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(x, y);
        }
        
        function stopDrawing() {
            if (!isDrawing) return;
            isDrawing = false;
            ctx.beginPath();
        }
        
        function changeColor(color) {
            currentColor = color;
        }
        
        function changeBrushSize(size) {
            currentSize = size;
        }
        
        function clearCanvas() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = 'white';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }
    </script>
    """
    
    st.components.v1.html(drawing_code, height=600)
    
    # Back button
    if st.button("Back to Menu", key="drawing_back"):
        back_to_menu()
        st.experimental_rerun()

def shapes_game():
    """Shape recognition game implementation"""
    st.markdown('<h1 class="game-title">Shape Recognition</h1>', unsafe_allow_html=True)
    
    # Generate random shapes
    if 'shapes_game_objects' not in st.session_state or 'target_shape' not in st.session_state:
        shape_types = ['circle', 'square', 'triangle', 'star', 'rectangle', 'diamond']
        colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
        
        target_shape = random.choice(shape_types)
        objects = []
        
        # Generate 6-10 random shapes
        num_shapes = random.randint(6, 10)
        for _ in range(num_shapes):
            shape_type = random.choice(shape_types)
            color = random.choice(colors)
            size = random.randint(40, 80)
            objects.append((shape_type, color, size))
        
        # Ensure at least one target shape exists
        if not any(obj[0] == target_shape for obj in objects):
            idx = random.randint(0, len(objects) - 1)
            objects[idx] = (target_shape, objects[idx][1], objects[idx][2])
        
        st.session_state.shapes_game_objects = objects
        st.session_state.target_shape = target_shape
        st.session_state.shapes_feedback = None
        st.session_state.found_shapes = []
    
    # Display the question
    st.markdown(f'<h2>Find all the {st.session_state.target_shape}s!</h2>', unsafe_allow_html=True)
    
    # Display the shapes
    cols = st.columns(5)
    for i, (shape_type, color, size) in enumerate(st.session_state.shapes_game_objects):
        with cols[i % 5]:
            # Create a unique key for each shape button
            shape_key = f"shape_{i}"
            
            # Skip if this shape has already been found
            if i in st.session_state.found_shapes:
                st.markdown(f'<div style="width:100px;height:100px;margin:10px auto;opacity:0.3;"></div>', unsafe_allow_html=True)
                continue
            
            # Create a button for each shape
            if shape_type == 'circle':
                shape_html = f'<div style="width:{size}px;height:{size}px;background-color:{color};border-radius:50%;margin:10px auto;"></div>'
            elif shape_type == 'square':
                shape_html = f'<div style="width:{size}px;height:{size}px;background-color:{color};margin:10px auto;"></div>'
            elif shape_type == 'rectangle':
                shape_html = f'<div style="width:{size}px;height:{size//2}px;background-color:{color};margin:10px auto;"></div>'
            elif shape_type == 'triangle':
                shape_html = f'<div style="width:0;height:0;border-left:{size//2}px solid transparent;border-right:{size//2}px solid transparent;border-bottom:{size}px solid {color};margin:10px auto;"></div>'
            elif shape_type == 'star':
                shape_html = f'<div style="font-size:{size}px;color:{color};text-align:center;margin:10px auto;">⭐</div>'
            elif shape_type == 'diamond':
                shape_html = f'<div style="width:0;height:0;border-left:{size//2}px solid transparent;border-right:{size//2}px solid transparent;border-bottom:{size}px solid {color};margin:10px auto;position:relative;"></div><div style="width:0;height:0;border-left:{size//2}px solid transparent;border-right:{size//2}px solid transparent;border-top:{size}px solid {color};margin-top:-{size//2}px;position:relative;"></div>'
            
            # Use a button with the shape as HTML
            if st.button(shape_html, key=shape_key):
                if shape_type == st.session_state.target_shape:
                    st.session_state.shapes_score += 1
                    st.session_state.shapes_feedback = f"Correct! That's a {shape_type}! 🎉"
                    st.session_state.mascot_message = "Great job finding the shapes!"
                    st.session_state.found_shapes.append(i)
                    
                    # Check if all target shapes have been found
                    target_shapes = [i for i, (s, _, _) in enumerate(st.session_state.shapes_game_objects) if s == st.session_state.target_shape]
                    if all(idx in st.session_state.found_shapes for idx in target_shapes):
                        st.session_state.shapes_feedback = f"Amazing! You found all the {st.session_state.target_shape}s! 🎉"
                        # Generate new shapes after a delay
                        time.sleep(2)
                        del st.session_state.shapes_game_objects
                        del st.session_state.target_shape
                        st.session_state.found_shapes = []
                else:
                    st.session_state.shapes_feedback = f"That's not a {st.session_state.target_shape}. Try again!"
                    st.session_state.mascot_message = "Look carefully at the shapes!"
                st.experimental_rerun()
    
    # Display feedback
    if st.session_state.shapes_feedback:
        if "Correct" in st.session_state.shapes_feedback or "Amazing" in st.session_state.shapes_feedback:
            st.markdown(f'<div style="color:green;font-size:1.5rem;text-align:center;">{st.session_state.shapes_feedback}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="color:red;font-size:1.5rem;text-align:center;">{st.session_state.shapes_feedback}</div>', unsafe_allow_html=True)
    
    # Display score
    display_score("shapes")
    
    # Back button
    if st.button("Back to Menu", key="shapes_back"):
        back_to_menu()
        st.experimental_rerun()

def reward_screen():
    """Reward screen after completing activities"""
    st.markdown('<h1 class="main-header">Congratulations! 🎉</h1>', unsafe_allow_html=True)
    
    total_score = st.session_state.counting_score + st.session_state.alphabet_score + st.session_state.shapes_score
    
    # Display certificate
    st.markdown(f"""
    <div class="game-container">
        <h2 style="text-align:center;color:#4ECDC4;">Certificate of Achievement</h2>
        <p style="font-size:1.5rem;text-align:center;">For excellent performance in learning!</p>
        <div style="text-align:center;margin:20px 0;">
            <span class="star">⭐</span>
            <span class="star">⭐</span>
            <span class="star">⭐</span>
        </div>
        <h3 style="text-align:center;">Total Score: {total_score}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display mascot with congratulatory message
    display_mascot("You're a learning superstar! Keep up the great work!")
    
    # Back to menu button
    if st.button("Back to Menu", key="reward_back"):
        st.session_state.show_reward = False
        back_to_menu()
        st.experimental_rerun()

# Main application
def main():
    # Display header
    st.markdown('<h1 class="main-header">Kids Learning Adventure</h1>', unsafe_allow_html=True)
    
    # Show reward screen if requested
    if st.session_state.show_reward:
        reward_screen()
        return
    
    # Show the appropriate game based on selection
    if st.session_state.current_game == "counting":
        counting_game()
    elif st.session_state.current_game == "alphabet":
        alphabet_game()
    elif st.session_state.current_game == "drawing":
        drawing_game()
    elif st.session_state.current_game == "shapes":
        shapes_game()
    else:
        # Main menu
        display_mascot()
        
        st.markdown('<div class="game-container">', unsafe_allow_html=True)
        
        # Game selection buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Counting Game", key="menu_counting", help="Learn to count with colorful objects"):
                st.session_state.current_game = "counting"
                st.session_state.mascot_message = "Let's count together!"
                st.experimental_rerun()
            
            if st.button("Alphabet Learning", key="menu_alphabet", help="Learn the alphabet with fun examples"):
                st.session_state.current_game = "alphabet"
                st.session_state.mascot_message = "Time to learn the alphabet!"
                st.experimental_rerun()
        
        with col2:
            if st.button("Drawing Canvas", key="menu_drawing", help="Express your creativity with colors"):
                st.session_state.current_game = "drawing"
                st.session_state.mascot_message = "Express your creativity!"
                st.experimental_rerun()
            
            if st.button("Shape Recognition", key="menu_shapes", help="Learn to identify different shapes"):
                st.session_state.current_game = "shapes"
                st.session_state.mascot_message = "Can you find the shapes?"
                st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Total score and reward button
        total_score = st.session_state.counting_score + st.session_state.alphabet_score + st.session_state.shapes_score
        
        st.markdown(f"""
        <div class="score-display">
            Total Score: {total_score} {'<span class="star">⭐</span>' * (total_score // 10)}
        </div>
        """, unsafe_allow_html=True)
        
        if total_score >= 10:
            if st.button("View Certificate", key="view_certificate"):
                st.session_state.show_reward = True
                st.experimental_rerun()

if __name__ == "__main__":
    main()
