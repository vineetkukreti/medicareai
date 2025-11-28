import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';

const ChatBot = () => {
    const [messages, setMessages] = useState([
        {
            type: 'bot',
            text: "Hello! I'm MediCareAI, your personal health assistant. How can I help you today? You can ask me about symptoms, medications, general health advice, or any medical concerns you have.",
            timestamp: new Date()
        }
    ]);
    const [inputMessage, setInputMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState('');
    const messagesEndRef = useRef(null);

    useEffect(() => {
        // Generate session ID
        setSessionId(`session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
    }, []);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputMessage.trim() || isLoading) return;

        const userMessage = {
            type: 'user',
            text: inputMessage,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setIsLoading(true);

        // Add initial bot message for streaming
        const botMessageId = Date.now();
        setMessages(prev => [...prev, {
            type: 'bot',
            text: '',
            timestamp: new Date(),
            id: botMessageId,
            isStreaming: true
        }]);

        try {
            const response = await fetch('http://localhost:8000/api/chat/stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: inputMessage,
                    session_id: sessionId
                }),
            });

            if (!response.ok) throw new Error('Failed to get response');

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let botResponse = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                botResponse += chunk;

                setMessages(prev => prev.map(msg =>
                    msg.id === botMessageId
                        ? { ...msg, text: botResponse }
                        : msg
                ));
            }

            // Mark streaming as done
            setMessages(prev => prev.map(msg =>
                msg.id === botMessageId
                    ? { ...msg, isStreaming: false }
                    : msg
            ));

        } catch (error) {
            setMessages(prev => prev.map(msg =>
                msg.id === botMessageId
                    ? { ...msg, text: "I apologize, but I'm having trouble connecting right now. Please try again.", isStreaming: false }
                    : msg
            ));
        } finally {
            setIsLoading(false);
        }
    };

    const quickQuestions = [
        "What are the symptoms of flu?",
        "How to manage stress?",
        "Tips for better sleep",
        "When should I see a doctor?"
    ];

    const handleQuickQuestion = (question) => {
        setInputMessage(question);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50">
            {/* Header */}
            <nav className="bg-white/90 backdrop-blur-md border-b border-blue-100 shadow-sm sticky top-0 z-10">
                <div className="max-w-screen-xl mx-auto p-4 flex items-center justify-between">
                    <Link to="/" className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-lg flex items-center justify-center">
                            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                            </svg>
                        </div>
                        <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">MediCareAI</span>
                    </Link>
                    <Link to="/" className="text-blue-600 hover:text-blue-700 font-medium flex items-center">
                        <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                        Back to Home
                    </Link>
                </div>
            </nav>

            {/* Main Chat Container */}
            <div className="max-w-5xl mx-auto p-4 h-[calc(100vh-80px)] flex flex-col">
                {/* Chat Header */}
                <div className="bg-white rounded-t-2xl p-6 border-b border-blue-100 shadow-sm">
                    <div className="flex items-center space-x-4">
                        <div className="w-14 h-14 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-full flex items-center justify-center shadow-lg">
                            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                            </svg>
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-gray-900">AI Medical Assistant</h1>
                            <p className="text-sm text-gray-600 flex items-center">
                                <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
                                Online and ready to help
                            </p>
                        </div>
                    </div>
                </div>

                {/* Messages Container */}
                <div className="flex-1 bg-white p-6 overflow-y-auto space-y-4">
                    {messages.map((message, index) => (
                        <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`flex items-start space-x-2 max-w-3xl ${message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                                {/* Avatar */}
                                <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${message.type === 'user'
                                    ? 'bg-gradient-to-br from-purple-600 to-pink-500'
                                    : 'bg-gradient-to-br from-blue-600 to-cyan-500'
                                    }`}>
                                    {message.type === 'user' ? (
                                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                        </svg>
                                    ) : (
                                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                                        </svg>
                                    )}
                                </div>

                                {/* Message Bubble */}
                                <div className={`rounded-2xl px-5 py-3 shadow-sm ${message.type === 'user'
                                    ? 'bg-gradient-to-r from-purple-600 to-pink-500 text-white'
                                    : 'bg-gray-100 text-gray-900'
                                    }`}>
                                    <p className="text-sm leading-relaxed whitespace-pre-wrap">
                                        {message.text}
                                        {message.isStreaming && <span className="inline-block w-2 h-4 ml-1 bg-blue-500 animate-pulse align-middle"></span>}
                                    </p>
                                    <p className={`text-xs mt-2 ${message.type === 'user' ? 'text-purple-200' : 'text-gray-500'}`}>
                                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </p>
                                </div>
                            </div>
                        </div>
                    ))}

                    {isLoading && (
                        <div className="flex justify-start">
                            <div className="flex items-start space-x-2 max-w-3xl">
                                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-cyan-500 rounded-full flex items-center justify-center">
                                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                                    </svg>
                                </div>
                                <div className="bg-gray-100 rounded-2xl px-5 py-3 shadow-sm">
                                    <div className="flex space-x-2">
                                        <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
                                        <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce delay-100"></div>
                                        <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce delay-200"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Quick Questions */}
                {messages.length === 1 && (
                    <div className="bg-white px-6 py-4 border-t border-blue-100">
                        <p className="text-sm text-gray-600 mb-3 font-medium">Quick questions to get started:</p>
                        <div className="flex flex-wrap gap-2">
                            {quickQuestions.map((question, index) => (
                                <button
                                    key={index}
                                    onClick={() => handleQuickQuestion(question)}
                                    className="px-4 py-2 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-full text-sm font-medium transition-colors border border-blue-200"
                                >
                                    {question}
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {/* Input Area */}
                <div className="bg-white rounded-b-2xl p-6 border-t border-blue-100 shadow-lg">
                    <form onSubmit={handleSendMessage} className="flex space-x-3">
                        <input
                            type="text"
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                            placeholder="Type your health question here..."
                            className="flex-1 px-5 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            disabled={isLoading}
                        />
                        <button
                            type="submit"
                            disabled={isLoading || !inputMessage.trim()}
                            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-500 text-white rounded-full font-semibold hover:from-blue-700 hover:to-cyan-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                            </svg>
                        </button>
                    </form>
                    <p className="text-xs text-gray-500 mt-3 text-center">
                        ⚠️ This AI assistant provides general information only. Always consult a healthcare professional for medical advice.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default ChatBot;
