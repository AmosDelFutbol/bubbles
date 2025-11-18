import streamlit as st
import os
import sys
import base64
import time
import threading
import socket
from io import BytesIO

# HTML content for the Bluey-themed educational games platform
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>Bluey's Learning Adventure</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: 'Comic Sans MS', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #87CEEB 0%, #98D8E8 50%, #B0E0E6 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            position: fixed;
            width: 100%;
            height: 100%;
        }

        /* Main Menu Styles */
        .main-menu {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            padding: 2rem;
            z-index: 100;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><circle cx="20" cy="20" r="15" fill="%23ffffff" opacity="0.2"/><circle cx="80" cy="20" r="10" fill="%23ffffff" opacity="0.2"/><circle cx="50" cy="50" r="20" fill="%23ffffff" opacity="0.2"/><circle cx="20" cy="80" r="12" fill="%23ffffff" opacity="0.2"/><circle cx="80" cy="80" r="8" fill="%23ffffff" opacity="0.2"/></svg>') repeat;
            background-size: 200px 200px;
        }

        .main-title {
            font-size: 3rem;
            color: #0066CC;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 0px rgba(255,255,255,0.7);
            text-align: center;
        }

        .bluey-character {
            width: 120px;
            height: 120px;
            background: #0066CC;
            border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
            position: relative;
            margin-bottom: 2rem;
        }

        .bluey-character::before {
            content: '';
            position: absolute;
            width: 15px;
            height: 15px;
            background: white;
            border-radius: 50%;
            top: 40px;
            left: 30px;
        }

        .bluey-character::after {
            content: '';
            position: absolute;
            width: 15px;
            height: 15px;
            background: white;
            border-radius: 50%;
            top: 40px;
            right: 30px;
        }

        .bluey-nose {
            position: absolute;
            width: 10px;
            height: 10px;
            background: #333;
            border-radius: 50%;
            top: 60px;
            left: 55px;
        }

        .game-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            width: 100%;
            max-width: 800px;
        }

        .game-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .game-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
        }

        .game-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        .game-title {
            font-size: 1.5rem;
            color: #0066CC;
            margin-bottom: 0.5rem;
        }

        .game-description {
            font-size: 1rem;
            color: #555;
        }

        /* Game Screen Styles */
        .game-screen {
            display: none;
            flex-direction: column;
            height: 100vh;
            padding: 1rem;
        }

        .game-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.9);
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        .game-title-bar {
            font-size: 1.5rem;
            color: #0066CC;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .back-button {
            background: #FF9E80;
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        .game-content {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
        }

        /* Win Screen Styles */
        .win-screen {
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            padding: 2rem;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><circle cx="20" cy="20" r="15" fill="%23FFD700" opacity="0.2"/><circle cx="80" cy="20" r="10" fill="%23FFD700" opacity="0.2"/><circle cx="50" cy="50" r="20" fill="%23FFD700" opacity="0.2"/><circle cx="20" cy="80" r="12" fill="%23FFD700" opacity="0.2"/><circle cx="80" cy="80" r="8" fill="%23FFD700" opacity="0.2"/></svg>') repeat;
            background-size: 200px 200px;
        }

        .win-message {
            font-size: 3rem;
            color: #FF9E80;
            margin-bottom: 2rem;
            text-align: center;
            animation: bounce 1s ease infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }

        .win-buttons {
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            justify-content: center;
        }

        .win-button {
            background: #0066CC;
            color: white;
            border: none;
            border-radius: 25px;
            padding: 1rem 2rem;
            font-size: 1.2rem;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }

        .win-button:hover {
            transform: translateY(-5px);
        }

        /* Bubble Game Styles */
        .bubble-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(70px, 1fr));
            gap: 10px;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            backdrop-filter: blur(5px);
            max-width: 1200px;
            width: 100%;
        }

        .bubble {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 1.2rem;
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 0px rgba(0,0,0,0.2);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            -webkit-user-select: none;
            user-select: none;
        }

        .bubble::before {
            content: '';
            position: absolute;
            top: 10%;
            left: 20%;
            width: 40%;
            height: 40%;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.8), transparent);
            border-radius: 50%;
        }

        .bubble:hover:not(.popped) {
            transform: scale(1.1);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
        }

        .bubble.popped {
            animation: pop 0.4s ease-out forwards;
            pointer-events: none;
        }

        @keyframes pop {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.3);
                opacity: 0.5;
            }
            100% {
                transform: scale(0);
                opacity: 0;
            }
        }

        /* Shape Game Styles */
        .shape-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 1.5rem;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            backdrop-filter: blur(5px);
            max-width: 800px;
            width: 100%;
        }

        .shape {
            width: 100px;
            height: 100px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 1.2rem;
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 0px rgba(0,0,0,0.2);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            -webkit-user-select: none;
            user-select: none;
        }

        .shape:hover:not(.matched) {
            transform: scale(1.1);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
        }

        .shape.matched {
            animation: match 0.4s ease-out forwards;
            pointer-events: none;
        }

        @keyframes match {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.3);
                opacity: 0.5;
            }
            100% {
                transform: scale(0);
                opacity: 0;
            }
        }

        .circle {
            background: #FF9E80;
            border-radius: 50%;
        }

        .square {
            background: #80D8FF;
            border-radius: 10px;
        }

        .triangle {
            width: 0;
            height: 0;
            border-left: 50px solid transparent;
            border-right: 50px solid transparent;
            border-bottom: 100px solid #AED581;
            background: transparent;
            box-shadow: none;
        }

        .star {
            background: #FFD54F;
            clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
        }

        .heart {
            background: #FF8A80;
            position: relative;
            transform: rotate(-45deg);
            width: 80px;
            height: 80px;
            margin: 20px;
        }

        .heart:before,
        .heart:after {
            content: "";
            position: absolute;
            width: 80px;
            height: 80px;
            background: #FF8A80;
            border-radius: 50%;
        }

        .heart:before {
            top: -40px;
            left: 0;
        }

        .heart:after {
            top: 0;
            left: 40px;
        }

        /* Color Game Styles */
        .color-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 1.5rem;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            backdrop-filter: blur(5px);
            max-width: 800px;
            width: 100%;
        }

        .color-item {
            width: 100px;
            height: 100px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 1.2rem;
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 0px rgba(0,0,0,0.2);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            -webkit-user-select: none;
            user-select: none;
            border-radius: 15px;
        }

        .color-item:hover:not(.matched) {
            transform: scale(1.1);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
        }

        .color-item.matched {
            animation: match 0.4s ease-out forwards;
            pointer-events: none;
        }

        .red { background: #FF5252; }
        .blue { background: #448AFF; }
        .green { background: #69F0AE; }
        .yellow { background: #FFD740; }
        .orange { background: #FF9100; }
        .purple { background: #E040FB; }
        .pink { background: #FF4081; }
        .brown { background: #795548; }

        /* Animal Game Styles */
        .animal-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1.5rem;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            backdrop-filter: blur(5px);
            max-width: 800px;
            width: 100%;
        }

        .animal-item {
            width: 120px;
            height: 120px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-size: 1.2rem;
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 0px rgba(0,0,0,0.2);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            -webkit-user-select: none;
            user-select: none;
            border-radius: 15px;
            background: rgba(255, 255, 255, 0.9);
        }

        .animal-icon {
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }

        .animal-name {
            color: #0066CC;
            font-size: 1rem;
        }

        .animal-item:hover:not(.matched) {
            transform: scale(1.1);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
        }

        .animal-item.matched {
            animation: match 0.4s ease-out forwards;
            pointer-events: none;
        }

        /* Settings Panel */
        .settings-panel {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 1.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            display: none;
            min-width: 280px;
            max-width: 90%;
        }

        .settings-panel.active {
            display: block;
            animation: slideIn 0.3s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translate(-50%, -40%);
            }
            to {
                opacity: 1;
                transform: translate(-50%, -50%);
            }
        }

        .settings-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }

        .settings-title {
            font-size: 1.3rem;
            color: #0066CC;
        }

        .close-btn {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #999;
            padding: 0;
            width: 30px;
            height: 30px;
        }

        .setting-item {
            margin-bottom: 1rem;
        }

        .setting-label {
            display: block;
            margin-bottom: 0.5rem;
            color: #555;
            font-weight: 500;
        }

        input[type="range"] {
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: #ddd;
            outline: none;
            -webkit-appearance: none;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #0066CC;
            cursor: pointer;
        }

        input[type="range"]::-moz-range-thumb {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #0066CC;
            cursor: pointer;
        }

        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            z-index: 999;
            display: none;
        }

        .overlay.active {
            display: block;
        }

        /* Language Selector */
        .language-selector {
            display: flex;
            gap: 0.5rem;
            background: white;
            padding: 0.25rem;
            border-radius: 25px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

        .lang-btn {
            padding: 0.5rem 0.75rem;
            border: none;
            border-radius: 20px;
            background: transparent;
            color: #0066CC;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            font-size: 0.8rem;
        }

        .lang-btn.active {
            background: #0066CC;
            color: white;
        }

        /* Mobile Responsive */
        @media (max-width: 768px) {
            .main-title {
                font-size: 2rem;
            }
            
            .game-grid {
                grid-template-columns: 1fr;
            }
            
            .bubble {
                width: 60px;
                height: 60px;
                font-size: 1rem;
            }
            
            .bubble-container {
                gap: 8px;
                padding: 0.5rem;
            }
            
            .shape, .color-item {
                width: 80px;
                height: 80px;
            }
            
            .animal-item {
                width: 100px;
                height: 100px;
            }
            
            .animal-icon {
                font-size: 2.5rem;
            }
        }
    </style>
</head>
<body>
    <!-- Main Menu -->
    <div class="main-menu" id="mainMenu">
        <div class="bluey-character">
            <div class="bluey-nose"></div>
        </div>
        <h1 class="main-title">Bluey's Learning Adventure</h1>
        <div class="game-grid">
            <div class="game-card" onclick="startGame('bubble')">
                <div class="game-icon">🫧</div>
                <div class="game-title">Bubble Pop</div>
                <div class="game-description">Pop bubbles and learn numbers and letters!</div>
            </div>
            <div class="game-card" onclick="startGame('shape')">
                <div class="game-icon">🔷</div>
                <div class="game-title">Shape Match</div>
                <div class="game-description">Match the shapes to learn geometry!</div>
            </div>
            <div class="game-card" onclick="startGame('color')">
                <div class="game-icon">🎨</div>
                <div class="game-title">Color Fun</div>
                <div class="game-description">Learn colors with fun activities!</div>
            </div>
            <div class="game-card" onclick="startGame('animal')">
                <div class="game-icon">🐾</div>
                <div class="game-title">Animal Friends</div>
                <div class="game-description">Meet and learn about different animals!</div>
            </div>
        </div>
    </div>

    <!-- Game Screen -->
    <div class="game-screen" id="gameScreen">
        <div class="game-header">
            <div class="game-title-bar">
                <div class="game-icon" id="gameIcon">🫧</div>
                <div id="gameTitle">Bubble Pop</div>
            </div>
            <div class="language-selector">
                <button class="lang-btn active" onclick="setLanguage('en')">EN</button>
                <button class="lang-btn" onclick="setLanguage('es')">ES</button>
            </div>
            <button class="back-button" onclick="backToMenu()">Back to Menu</button>
        </div>
        <div class="game-content" id="gameContent">
            <!-- Game content will be dynamically inserted here -->
        </div>
    </div>

    <!-- Win Screen -->
    <div class="win-screen" id="winScreen">
        <div class="win-message">🎉 You Win! 🎉</div>
        <div class="win-buttons">
            <button class="win-button" onclick="playAgain()">Play Again</button>
            <button class="win-button" onclick="backToMenu()">Choose Another Game</button>
        </div>
    </div>

    <!-- Settings Panel -->
    <div class="overlay" id="overlay" onclick="toggleSettings()"></div>
    <div class="settings-panel" id="settingsPanel">
        <div class="settings-header">
            <h2 class="settings-title">Settings</h2>
            <button class="close-btn" onclick="toggleSettings()">×</button>
        </div>
        <div class="setting-item">
            <label class="setting-label">Sound Volume</label>
            <input type="range" id="soundVolume" min="0" max="100" value="50" onchange="updateVolume(this.value)">
        </div>
    </div>

    <script>
        // Game state
        let audioContext;
        let masterGainNode;
        let volume = 0.5;
        let currentGame = null;
        let language = 'en'; // 'en', 'es'
        let gameItems = [];
        let matchedItems = 0;
        let totalItems = 0;

        // Spanish translations
        const spanishNumbers = [
            'uno', 'dos', 'tres', 'cuatro', 'cinco', 
            'seis', 'siete', 'ocho', 'nueve', 'diez',
            'once', 'doce', 'trece', 'catorce', 'quince',
            'dieciséis', 'diecisiete', 'dieciocho', 'diecinueve', 'veinte'
        ];

        const spanishAlphabet = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
            'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
        ];

        const englishAlphabet = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
        ];

        const spanishColors = {
            'red': 'rojo',
            'blue': 'azul',
            'green': 'verde',
            'yellow': 'amarillo',
            'orange': 'naranja',
            'purple': 'púrpura',
            'pink': 'rosa',
            'brown': 'marrón'
        };

        const spanishAnimals = {
            'dog': 'perro',
            'cat': 'gato',
            'bird': 'pájaro',
            'fish': 'pez',
            'rabbit': 'conejo',
            'turtle': 'tortuga',
            'butterfly': 'mariposa',
            'elephant': 'elefante'
        };

        const spanishShapes = {
            'circle': 'círculo',
            'square': 'cuadrado',
            'triangle': 'triángulo',
            'star': 'estrella',
            'heart': 'corazón'
        };

        // Initialize audio context (needed for iPhone)
        function initAudio() {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                masterGainNode = audioContext.createGain();
                masterGainNode.connect(audioContext.destination);
                masterGainNode.gain.value = volume;
            }
            
            // Resume audio context if suspended (iOS requirement)
            if (audioContext.state === 'suspended') {
                audioContext.resume();
            }
        }

        // Generate pop sound
        function playPopSound(frequency = 800, duration = 0.1) {
            if (!audioContext) return;
            
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(masterGainNode);
            
            oscillator.frequency.value = frequency;
            oscillator.type = 'sine';
            
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + duration);
        }

        // Text-to-speech for numbers and letters
        function speakText(text) {
            if ('speechSynthesis' in window) {
                // Cancel any ongoing speech
                window.speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = language === 'es' ? 'es-ES' : 'en-US';
                utterance.rate = 0.8;
                utterance.pitch = 1.2;
                utterance.volume = volume;
                
                window.speechSynthesis.speak(utterance);
            }
        }

        // Create particle effect
        function createParticles(x, y, count = 8) {
            for (let i = 0; i < count; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = x + 'px';
                particle.style.top = y + 'px';
                
                // Random color for particles
                const colors = ['#FF9E80', '#80D8FF', '#AED581', '#FFD54F', '#FF8A80'];
                const color = colors[Math.floor(Math.random() * colors.length)];
                particle.style.background = color;
                particle.style.width = '15px';
                particle.style.height = '15px';
                particle.style.borderRadius = '50%';
                particle.style.position = 'fixed';
                particle.style.pointerEvents = 'none';
                
                const angle = (Math.PI * 2 * i) / count;
                const velocity = 50 + Math.random() * 50;
                particle.style.setProperty('--tx', Math.cos(angle) * velocity + 'px');
                particle.style.setProperty('--ty', Math.sin(angle) * velocity + 'px');
                particle.style.animation = 'particle-fly 0.8s ease-out forwards';
                
                document.body.appendChild(particle);
                
                setTimeout(() => particle.remove(), 800);
            }
        }

        // Start a game
        function startGame(gameType) {
            currentGame = gameType;
            matchedItems = 0;
            
            // Hide main menu, show game screen
            document.getElementById('mainMenu').style.display = 'none';
            document.getElementById('gameScreen').style.display = 'flex';
            document.getElementById('winScreen').style.display = 'none';
            
            // Set game title and icon
            const gameInfo = {
                'bubble': { icon: '🫧', title: 'Bubble Pop' },
                'shape': { icon: '🔷', title: 'Shape Match' },
                'color': { icon: '🎨', title: 'Color Fun' },
                'animal': { icon: '🐾', title: 'Animal Friends' }
            };
            
            document.getElementById('gameIcon').textContent = gameInfo[gameType].icon;
            document.getElementById('gameTitle').textContent = gameInfo[gameType].title;
            
            // Initialize the game
            initAudio();
            
            // Load game content
            switch(gameType) {
                case 'bubble':
                    loadBubbleGame();
                    break;
                case 'shape':
                    loadShapeGame();
                    break;
                case 'color':
                    loadColorGame();
                    break;
                case 'animal':
                    loadAnimalGame();
                    break;
            }
        }

        // Load Bubble Game
        function loadBubbleGame() {
            const gameContent = document.getElementById('gameContent');
            gameContent.innerHTML = '<div class="bubble-container" id="bubbleContainer"></div>';
            
            const container = document.getElementById('bubbleContainer');
            container.innerHTML = '';
            
            // Adjust bubble count for mobile
            const isMobile = window.innerWidth < 768;
            const bubbleCount = isMobile ? 24 : 36;
            totalItems = bubbleCount;
            
            // Create mode selector
            const modeSelector = document.createElement('div');
            modeSelector.style.display = 'flex';
            modeSelector.style.justifyContent = 'center';
            modeSelector.style.marginBottom = '1rem';
            modeSelector.style.gap = '1rem';
            
            const funBtn = document.createElement('button');
            funBtn.textContent = 'Fun';
            funBtn.className = 'lang-btn active';
            funBtn.onclick = () => setBubbleMode('fun');
            
            const countBtn = document.createElement('button');
            countBtn.textContent = 'Count';
            countBtn.className = 'lang-btn';
            countBtn.onclick = () => setBubbleMode('count');
            
            const abcBtn = document.createElement('button');
            abcBtn.textContent = 'ABC';
            abcBtn.className = 'lang-btn';
            abcBtn.onclick = () => setBubbleMode('abc');
            
            modeSelector.appendChild(funBtn);
            modeSelector.appendChild(countBtn);
            modeSelector.appendChild(abcBtn);
            
            gameContent.insertBefore(modeSelector, container);
            
            let currentNumber = 1;
            let currentLetter = 0;
            let bubbleMode = 'fun';
            
            // Set bubble mode function
            window.setBubbleMode = function(mode) {
                bubbleMode = mode;
                currentNumber = 1;
                currentLetter = 0;
                
                // Update button states
                document.querySelectorAll('.lang-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                event.target.classList.add('active');
                
                // Reload bubbles
                container.innerHTML = '';
                createBubbles();
            };
            
            // Create bubbles function
            function createBubbles() {
                container.innerHTML = '';
                
                for (let i = 0; i < bubbleCount; i++) {
                    const bubble = document.createElement('div');
                    bubble.className = 'bubble';
                    
                    // Set background color
                    const colors = [
                        '#FF9E80', '#80D8FF', '#AED581', '#FFD54F', '#FF8A80'
                    ];
                    const colorIndex = i % colors.length;
                    bubble.style.background = colors[colorIndex];
                    
                    // Add content based on mode and language
                    if (bubbleMode === 'count') {
                        if (language === 'es') {
                            bubble.textContent = spanishNumbers[currentNumber - 1];
                        } else {
                            bubble.textContent = currentNumber;
                        }
                        currentNumber++;
                        if (currentNumber > 20) currentNumber = 1;
                    } else if (bubbleMode === 'abc') {
                        if (language === 'es') {
                            bubble.textContent = spanishAlphabet[currentLetter];
                        } else {
                            bubble.textContent = englishAlphabet[currentLetter];
                        }
                        currentLetter++;
                        if (language === 'es' && currentLetter >= spanishAlphabet.length) {
                            currentLetter = 0;
                        } else if (language === 'en' && currentLetter >= englishAlphabet.length) {
                            currentLetter = 0;
                        }
                    }
                    
                    // Add click event
                    bubble.addEventListener('click', (e) => {
                        if (bubble.classList.contains('popped')) return;
                        
                        bubble.classList.add('popped');
                        
                        // Create particles at bubble position
                        const rect = bubble.getBoundingClientRect();
                        createParticles(rect.left + rect.width / 2, rect.top + rect.height / 2);
                        
                        // Play pop sound
                        playPopSound(800 + Math.random() * 400, 0.1);
                        
                        // Speak the content if in educational mode
                        if (bubbleMode === 'count' || bubbleMode === 'abc') {
                            const content = bubble.textContent;
                            speakText(content);
                        }
                        
                        // Check if all bubbles are popped
                        matchedItems++;
                        if (matchedItems >= totalItems) {
                            setTimeout(showWinScreen, 500);
                        }
                    });
                    
                    container.appendChild(bubble);
                }
            }
            
            // Initial bubble creation
            createBubbles();
        }

        // Load Shape Game
        function loadShapeGame() {
            const gameContent = document.getElementById('gameContent');
            gameContent.innerHTML = '<div class="shape-container" id="shapeContainer"></div>';
            
            const container = document.getElementById('shapeContainer');
            container.innerHTML = '';
            
            const shapes = ['circle', 'square', 'triangle', 'star', 'heart'];
            const shapeNames = language === 'es' ? spanishShapes : {
                'circle': 'circle',
                'square': 'square',
                'triangle': 'triangle',
                'star': 'star',
                'heart': 'heart'
            };
            
            // Create pairs of shapes (for matching)
            const shapePairs = [];
            shapes.forEach(shape => {
                shapePairs.push(shape, shape); // Add each shape twice
            });
            
            // Shuffle the shapes
            shapePairs.sort(() => Math.random() - 0.5);
            
            totalItems = shapePairs.length;
            let firstShape = null;
            let secondShape = null;
            let canClick = true;
            
            shapePairs.forEach((shape, index) => {
                const shapeElement = document.createElement('div');
                shapeElement.className = `shape ${shape}`;
                shapeElement.dataset.shape = shape;
                
                // Special handling for triangle and heart
                if (shape === 'triangle' || shape === 'heart') {
                    shapeElement.innerHTML = `<div style="color:#333; text-shadow:1px 1px 0px rgba(255,255,255,0.7); font-weight:bold;">${shapeNames[shape]}</div>`;
                } else {
                    shapeElement.textContent = shapeNames[shape];
                }
                
                shapeElement.addEventListener('click', () => {
                    if (!canClick || shapeElement.classList.contains('matched')) return;
                    
                    if (!firstShape) {
                        firstShape = shapeElement;
                        shapeElement.style.outline = '3px solid #FFD54F';
                        speakText(shapeNames[shape]);
                    } else if (!secondShape && shapeElement !== firstShape) {
                        secondShape = shapeElement;
                        shapeElement.style.outline = '3px solid #FFD54F';
                        
                        canClick = false;
                        
                        // Check if shapes match
                        setTimeout(() => {
                            if (firstShape.dataset.shape === secondShape.dataset.shape) {
                                // Match found
                                firstShape.classList.add('matched');
                                secondShape.classList.add('matched');
                                playPopSound(1200, 0.2);
                                createParticles(
                                    firstShape.getBoundingClientRect().left + firstShape.offsetWidth / 2,
                                    firstShape.getBoundingClientRect().top + firstShape.offsetHeight / 2,
                                    12
                                );
                                createParticles(
                                    secondShape.getBoundingClientRect().left + secondShape.offsetWidth / 2,
                                    secondShape.getBoundingClientRect().top + secondShape.offsetHeight / 2,
                                    12
                                );
                                
                                matchedItems += 2;
                                
                                if (matchedItems >= totalItems) {
                                    setTimeout(showWinScreen, 500);
                                }
                            } else {
                                // No match
                                playPopSound(400, 0.2);
                            }
                            
                            // Remove outlines
                            firstShape.style.outline = '';
                            secondShape.style.outline = '';
                            
                            firstShape = null;
                            secondShape = null;
                            canClick = true;
                        }, 1000);
                    }
                });
                
                container.appendChild(shapeElement);
            });
        }

        // Load Color Game
        function loadColorGame() {
            const gameContent = document.getElementById('gameContent');
            gameContent.innerHTML = '<div class="color-container" id="colorContainer"></div>';
            
            const container = document.getElementById('colorContainer');
            container.innerHTML = '';
            
            const colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown'];
            const colorNames = language === 'es' ? spanishColors : {
                'red': 'red',
                'blue': 'blue',
                'green': 'green',
                'yellow': 'yellow',
                'orange': 'orange',
                'purple': 'purple',
                'pink': 'pink',
                'brown': 'brown'
            };
            
            // Create pairs of colors (for matching)
            const colorPairs = [];
            colors.forEach(color => {
                colorPairs.push(color, color); // Add each color twice
            });
            
            // Shuffle the colors
            colorPairs.sort(() => Math.random() - 0.5);
            
            totalItems = colorPairs.length;
            let firstColor = null;
            let secondColor = null;
            let canClick = true;
            
            colorPairs.forEach((color, index) => {
                const colorElement = document.createElement('div');
                colorElement.className = `color-item ${color}`;
                colorElement.dataset.color = color;
                colorElement.textContent = colorNames[color];
                
                colorElement.addEventListener('click', () => {
                    if (!canClick || colorElement.classList.contains('matched')) return;
                    
                    if (!firstColor) {
                        firstColor = colorElement;
                        colorElement.style.outline = '3px solid #FFD54F';
                        speakText(colorNames[color]);
                    } else if (!secondColor && colorElement !== firstColor) {
                        secondColor = colorElement;
                        colorElement.style.outline = '3px solid #FFD54F';
                        
                        canClick = false;
                        
                        // Check if colors match
                        setTimeout(() => {
                            if (firstColor.dataset.color === secondColor.dataset.color) {
                                // Match found
                                firstColor.classList.add('matched');
                                secondColor.classList.add('matched');
                                playPopSound(1200, 0.2);
                                createParticles(
                                    firstColor.getBoundingClientRect().left + firstColor.offsetWidth / 2,
                                    firstColor.getBoundingClientRect().top + firstColor.offsetHeight / 2,
                                    12
                                );
                                createParticles(
                                    secondColor.getBoundingClientRect().left + secondColor.offsetWidth / 2,
                                    secondColor.getBoundingClientRect().top + secondColor.offsetHeight / 2,
                                    12
                                );
                                
                                matchedItems += 2;
                                
                                if (matchedItems >= totalItems) {
                                    setTimeout(showWinScreen, 500);
                                }
                            } else {
                                // No match
                                playPopSound(400, 0.2);
                            }
                            
                            // Remove outlines
                            firstColor.style.outline = '';
                            secondColor.style.outline = '';
                            
                            firstColor = null;
                            secondColor = null;
                            canClick = true;
                        }, 1000);
                    }
                });
                
                container.appendChild(colorElement);
            });
        }

        // Load Animal Game
        function loadAnimalGame() {
            const gameContent = document.getElementById('gameContent');
            gameContent.innerHTML = '<div class="animal-container" id="animalContainer"></div>';
            
            const container = document.getElementById('animalContainer');
            container.innerHTML = '';
            
            const animals = [
                { name: 'dog', icon: '🐕' },
                { name: 'cat', icon: '🐈' },
                { name: 'bird', icon: '🐦' },
                { name: 'fish', icon: '🐠' },
                { name: 'rabbit', icon: '🐰' },
                { name: 'turtle', icon: '🐢' },
                { name: 'butterfly', icon: '🦋' },
                { name: 'elephant', icon: '🐘' }
            ];
            
            const animalNames = language === 'es' ? spanishAnimals : {
                'dog': 'dog',
                'cat': 'cat',
                'bird': 'bird',
                'fish': 'fish',
                'rabbit': 'rabbit',
                'turtle': 'turtle',
                'butterfly': 'butterfly',
                'elephant': 'elephant'
            };
            
            // Create pairs of animals (for matching)
            const animalPairs = [];
            animals.forEach(animal => {
                animalPairs.push(animal, animal); // Add each animal twice
            });
            
            // Shuffle the animals
            animalPairs.sort(() => Math.random() - 0.5);
            
            totalItems = animalPairs.length;
            let firstAnimal = null;
            let secondAnimal = null;
            let canClick = true;
            
            animalPairs.forEach((animal, index) => {
                const animalElement = document.createElement('div');
                animalElement.className = 'animal-item';
                animalElement.dataset.animal = animal.name;
                
                const iconElement = document.createElement('div');
                iconElement.className = 'animal-icon';
                iconElement.textContent = animal.icon;
                
                const nameElement = document.createElement('div');
                nameElement.className = 'animal-name';
                nameElement.textContent = animalNames[animal.name];
                
                animalElement.appendChild(iconElement);
                animalElement.appendChild(nameElement);
                
                animalElement.addEventListener('click', () => {
                    if (!canClick || animalElement.classList.contains('matched')) return;
                    
                    if (!firstAnimal) {
                        firstAnimal = animalElement;
                        animalElement.style.outline = '3px solid #FFD54F';
                        speakText(animalNames[animal.name]);
                    } else if (!secondAnimal && animalElement !== firstAnimal) {
                        secondAnimal = animalElement;
                        animalElement.style.outline = '3px solid #FFD54F';
                        
                        canClick = false;
                        
                        // Check if animals match
                        setTimeout(() => {
                            if (firstAnimal.dataset.animal === secondAnimal.dataset.animal) {
                                // Match found
                                firstAnimal.classList.add('matched');
                                secondAnimal.classList.add('matched');
                                playPopSound(1200, 0.2);
                                createParticles(
                                    firstAnimal.getBoundingClientRect().left + firstAnimal.offsetWidth / 2,
                                    firstAnimal.getBoundingClientRect().top + firstAnimal.offsetHeight / 2,
                                    12
                                );
                                createParticles(
                                    secondAnimal.getBoundingClientRect().left + secondAnimal.offsetWidth / 2,
                                    secondAnimal.getBoundingClientRect().top + secondAnimal.offsetHeight / 2,
                                    12
                                );
                                
                                matchedItems += 2;
                                
                                if (matchedItems >= totalItems) {
                                    setTimeout(showWinScreen, 500);
                                }
                            } else {
                                // No match
                                playPopSound(400, 0.2);
                            }
                            
                            // Remove outlines
                            firstAnimal.style.outline = '';
                            secondAnimal.style.outline = '';
                            
                            firstAnimal = null;
                            secondAnimal = null;
                            canClick = true;
                        }, 1000);
                    }
                });
                
                container.appendChild(animalElement);
            });
        }

        // Show win screen
        function showWinScreen() {
            document.getElementById('gameScreen').style.display = 'none';
            document.getElementById('winScreen').style.display = 'flex';
            
            // Play celebration sound
            playPopSound(1000, 0.3);
            setTimeout(() => playPopSound(1200, 0.3), 200);
            setTimeout(() => playPopSound(1400, 0.3), 400);
            
            // Create celebration particles
            for (let i = 0; i < 20; i++) {
                setTimeout(() => {
                    createParticles(
                        Math.random() * window.innerWidth,
                        Math.random() * window.innerHeight,
                        10
                    );
                }, i * 100);
            }
            
            // Speak "You Win"
            if (language === 'es') {
                speakText('¡Ganaste!');
            } else {
                speakText('You Win!');
            }
        }

        // Play again
        function playAgain() {
            startGame(currentGame);
        }

        // Back to menu
        function backToMenu() {
            document.getElementById('mainMenu').style.display = 'flex';
            document.getElementById('gameScreen').style.display = 'none';
            document.getElementById('winScreen').style.display = 'none';
        }

        // Set language
        function setLanguage(lang) {
            language = lang;
            
            // Update UI
            document.querySelectorAll('.lang-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Restart current game if in game
            if (currentGame) {
                startGame(currentGame);
            }
        }

        // Settings functions
        function toggleSettings() {
            const panel = document.getElementById('settingsPanel');
            const overlay = document.getElementById('overlay');
            
            panel.classList.toggle('active');
            overlay.classList.toggle('active');
        }

        function updateVolume(value) {
            volume = value / 100;
            if (masterGainNode) {
                masterGainNode.gain.value = volume;
            }
        }

        // Initialize on load
        window.addEventListener('load', () => {
            // Add particle animation to CSS if not already there
            if (!document.querySelector('#particle-style')) {
                const style = document.createElement('style');
                style.id = 'particle-style';
                style.textContent = `
                    @keyframes particle-fly {
                        0% {
                            transform: translate(0, 0) scale(1);
                            opacity: 1;
                        }
                        100% {
                            transform: translate(var(--tx), var(--ty)) scale(0);
                            opacity: 0;
                        }
                    }
                `;
                document.head.appendChild(style);
            }
        });

        // Prevent scrolling on iOS
        document.addEventListener('touchmove', function(e) {
            if (e.target.closest('.game-content')) {
                e.preventDefault();
            }
        }, { passive: false });
    </script>
</body>
</html>"""

# Check if qrcode is available
try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

def generate_html_file():
    """Generate the HTML file for the Bluey learning games."""
    try:
        with open("bluey_learning_games.html", "w") as f:
            f.write(HTML_CONTENT)
        return True, "HTML file generated successfully!"
    except Exception as e:
        return False, f"Error generating HTML file: {str(e)}"

def generate_qr_code(url):
    """Generate a QR code for given URL."""
    if not QRCODE_AVAILABLE:
        return None, "QR code generation not available. Please install qrcode library."
    
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="#0066CC", back_color="white")
        
        # Convert to base64 for display in Streamlit
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str, "QR code generated successfully!"
    except Exception as e:
        return None, f"Error generating QR code: {str(e)}"

def get_local_ip():
    """Get the local IP address for network access."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

def main():
    st.set_page_config(
        page_title="Bluey's Learning Adventure",
        page_icon="🫧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🫧 Bluey's Learning Adventure - Streamlit Edition")
    st.markdown("---")
    
    # Display the game
    st.components.v1.html(HTML_CONTENT, height=800)
    
    # Instructions section
    with st.expander("How to Use on iPhone"):
        st.markdown("""
        ### Method 1: Direct Link
        1. Click the "Generate HTML File" button below
        2. Download the generated file
        3. Send it to your iPhone via email or AirDrop
        4. Open the file in Safari and tap the Share button
        5. Select "Add to Home Screen" to create an app icon
        
        ### Method 2: QR Code
        1. Click the "Generate QR Code" button below
        2. Scan the QR code with your iPhone's camera
        3. Tap the notification that appears to open the game
        4. Once open, tap the Share button and select "Add to Home Screen"
        """)
    
    # File generation section
    st.header("Generate Files")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Generate HTML File"):
            success, message = generate_html_file()
            if success:
                st.success(message)
                # Provide download link
                with open("bluey_learning_games.html", "r") as f:
                    st.download_button(
                        label="Download HTML File",
                        data=f.read(),
                        file_name="bluey_learning_games.html",
                        mime="text/html"
                    )
            else:
                st.error(message)
    
    with col2:
        if st.button("Generate QR Code"):
            # Get the current URL
            try:
                # Try to get the public URL if available
                public_url = st.experimental_get_query_params().get('url', [None])[0]
                if not public_url:
                    # Fallback to local IP
                    local_ip = get_local_ip()
                    public_url = f"http://{local_ip}:8501"
                
                qr_code, message = generate_qr_code(public_url)
                if qr_code:
                    st.success(message)
                    st.image(f"data:image/png;base64,{qr_code}", caption="Scan this QR code with your iPhone")
                else:
                    st.error(message)
            except Exception as e:
                st.error(f"Error generating QR code: {str(e)}")
    
    # Information section
    st.header("About the Games")
    st.markdown("""
    Bluey's Learning Adventure is a fun and educational game collection for kids that helps them learn:
    
    - **Number Recognition** (1-20)
    - **Alphabet Learning** (A-Z in English and Spanish)
    - **Shape Recognition** (circle, square, triangle, star, heart)
    - **Color Learning** (8 basic colors)
    - **Animal Recognition** (8 common animals)
    - **Bilingual Support** (English and Spanish)
    - **Memory Skills** (matching games)
    - **Motor Skills** (touching and interacting with elements)
    
    The games feature:
    - Bluey theme with kid-friendly design
    - Simplified voice feedback (just says the numbers/letters/shapes/colors/animals)
    - Full screen game experience
    - Win celebrations with the option to play again or choose a different game
    - Touch-optimized interface for mobile devices
    """)

if __name__ == "__main__":
    main()
