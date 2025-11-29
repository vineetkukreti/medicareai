import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

const ConsultationRoom = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [micOn, setMicOn] = useState(true);
    const [cameraOn, setCameraOn] = useState(true);
    const [messages, setMessages] = useState([
        { sender: 'system', text: 'Connecting to secure server...' },
        { sender: 'system', text: 'Dr. Wilson has joined the room.' },
        { sender: 'doctor', text: 'Hello! How can I help you today?' }
    ]);
    const [newMessage, setNewMessage] = useState('');
    const chatEndRef = useRef(null);

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = (e) => {
        e.preventDefault();
        if (!newMessage.trim()) return;

        setMessages([...messages, { sender: 'user', text: newMessage }]);
        setNewMessage('');

        // Simulate doctor response
        setTimeout(() => {
            setMessages(prev => [...prev, { sender: 'doctor', text: "I see. Could you describe your symptoms in more detail?" }]);
        }, 2000);
    };

    const handleEndCall = () => {
        if (window.confirm("Are you sure you want to end the consultation?")) {
            navigate('/health-dashboard');
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 text-white overflow-hidden flex flex-col">
            <Navbar />

            <div className="flex-1 pt-20 p-4 flex gap-4 h-screen box-border">
                {/* Main Video Area */}
                <div className="flex-1 flex flex-col gap-4">
                    <div className="flex-1 bg-gray-800 rounded-2xl relative overflow-hidden shadow-2xl border border-gray-700">
                        {/* Doctor's Video Feed (Placeholder) */}
                        <div className="absolute inset-0 flex items-center justify-center bg-gray-800">
                            <div className="text-center">
                                <div className="w-32 h-32 bg-gray-700 rounded-full mx-auto mb-4 flex items-center justify-center animate-pulse">
                                    <svg className="w-16 h-16 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                    </svg>
                                </div>
                                <h2 className="text-xl font-semibold text-gray-300">Dr. Sarah Wilson</h2>
                                <p className="text-sm text-green-400 mt-1 flex items-center justify-center gap-2">
                                    <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                                    Live Connection
                                </p>
                            </div>
                        </div>

                        {/* User's Self View */}
                        <div className="absolute bottom-4 right-4 w-48 h-36 bg-gray-900 rounded-xl border-2 border-gray-700 shadow-lg overflow-hidden">
                            {cameraOn ? (
                                <div className="w-full h-full bg-gray-800 flex items-center justify-center">
                                    <span className="text-xs text-gray-500">You</span>
                                </div>
                            ) : (
                                <div className="w-full h-full bg-black flex items-center justify-center">
                                    <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 3l18 18" />
                                    </svg>
                                </div>
                            )}
                        </div>

                        {/* Controls Overlay */}
                        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex items-center gap-4 bg-gray-900/80 backdrop-blur-md px-6 py-3 rounded-full border border-gray-700">
                            <button
                                onClick={() => setMicOn(!micOn)}
                                className={`p-4 rounded-full transition-all ${micOn ? 'bg-gray-700 hover:bg-gray-600 text-white' : 'bg-red-500 hover:bg-red-600 text-white'}`}
                            >
                                {micOn ? (
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                                    </svg>
                                ) : (
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
                                    </svg>
                                )}
                            </button>

                            <button
                                onClick={() => setCameraOn(!cameraOn)}
                                className={`p-4 rounded-full transition-all ${cameraOn ? 'bg-gray-700 hover:bg-gray-600 text-white' : 'bg-red-500 hover:bg-red-600 text-white'}`}
                            >
                                {cameraOn ? (
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                    </svg>
                                ) : (
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 3l18 18" />
                                    </svg>
                                )}
                            </button>

                            <button
                                onClick={handleEndCall}
                                className="p-4 rounded-full bg-red-600 hover:bg-red-700 text-white transition-all shadow-lg hover:shadow-red-500/30"
                            >
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 8l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2M5 3a2 2 0 00-2 2v1c0 8.284 6.716 15 15 15h1a2 2 0 002-2v-3.28a1 1 0 00-.684-.948l-4.493-1.498a1 1 0 00-1.21.502l-1.13 2.257a11.042 11.042 0 01-5.516-5.517l2.257-1.128a1 1 0 00.502-1.21L9.228 3.683A1 1 0 008.279 3H5z" />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>

                {/* Chat Sidebar */}
                <div className="w-80 bg-gray-800 rounded-2xl border border-gray-700 flex flex-col shadow-xl">
                    <div className="p-4 border-b border-gray-700">
                        <h3 className="font-semibold text-white">Consultation Chat</h3>
                        <p className="text-xs text-gray-400">Secure & Encrypted</p>
                    </div>

                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[85%] rounded-2xl px-4 py-2 text-sm ${msg.sender === 'user'
                                    ? 'bg-blue-600 text-white rounded-br-none'
                                    : msg.sender === 'system'
                                        ? 'bg-gray-700 text-gray-300 text-xs text-center w-full'
                                        : 'bg-gray-700 text-white rounded-bl-none'
                                    }`}>
                                    {msg.text}
                                </div>
                            </div>
                        ))}
                        <div ref={chatEndRef} />
                    </div>

                    <form onSubmit={handleSendMessage} className="p-4 border-t border-gray-700">
                        <div className="flex gap-2">
                            <input
                                type="text"
                                value={newMessage}
                                onChange={(e) => setNewMessage(e.target.value)}
                                placeholder="Type a message..."
                                className="flex-1 bg-gray-900 border border-gray-600 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500 transition-colors"
                            />
                            <button
                                type="submit"
                                className="p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl transition-colors"
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                                </svg>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default ConsultationRoom;
