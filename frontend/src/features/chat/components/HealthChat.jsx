import React, { useState, useRef, useEffect } from 'react';
import { Resizable } from 're-resizable';

const HealthChat = ({ userId }) => {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: "Hello! I'm your personal health assistant. I can analyze your health data to provide personalized insights. How can I help you today?"
        }
    ]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputText.trim() || isLoading) return;

        const userMessage = inputText.trim();
        setInputText('');

        // Add user message
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            // Get auth token from localStorage
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('Not authenticated');
            }

            const response = await fetch(`http://localhost:8000/api/insights/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ query: userMessage }),
            });

            if (!response.ok) {
                throw new Error('Failed to get response');
            }

            const data = await response.json();

            // Add AI response
            setMessages(prev => [...prev, { role: 'assistant', content: data.insight }]);
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: "I'm sorry, I encountered an error while processing your request. Please try again later."
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Resizable
            defaultSize={{
                width: '100%',
                height: 600,
            }}
            minWidth="400px"
            minHeight="400px"
            maxWidth="100%"
            maxHeight="800px"
            enable={{
                top: false,
                right: true,
                bottom: true,
                left: true,
                topRight: false,
                bottomRight: true,
                bottomLeft: true,
                topLeft: false
            }}
            style={{
                display: 'flex',
                flexDirection: 'column',
            }}
            handleStyles={{
                left: {
                    width: '8px',
                    left: '-4px',
                    cursor: 'ew-resize',
                },
                right: {
                    width: '8px',
                    right: '-4px',
                    cursor: 'ew-resize',
                },
                bottom: {
                    height: '8px',
                    bottom: '-4px',
                    cursor: 'ns-resize',
                },
                bottomRight: {
                    width: '16px',
                    height: '16px',
                    right: '-8px',
                    bottom: '-8px',
                    cursor: 'nwse-resize',
                    zIndex: 10,
                },
                bottomLeft: {
                    width: '16px',
                    height: '16px',
                    left: '-8px',
                    bottom: '-8px',
                    cursor: 'nesw-resize',
                    zIndex: 10,
                }
            }}
            handleClasses={{
                bottomRight: 'hover:bg-teal-500 transition-colors',
                bottomLeft: 'hover:bg-teal-500 transition-colors'
            }}
        >
            <div className="flex flex-col h-full bg-white rounded-2xl shadow-xl border border-teal-100 overflow-hidden">
                {/* Chat Header */}
                <div className="bg-gradient-to-r from-teal-600 to-cyan-500 p-4 text-white">
                    <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
                            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                        </div>
                        <div>
                            <h3 className="font-semibold text-lg">AI Health Assistant</h3>
                            <p className="text-teal-100 text-sm">Powered by your health data</p>
                        </div>
                    </div>
                </div>

                {/* Messages Area */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[85%] p-0 rounded-2xl overflow-hidden shadow-sm ${msg.role === 'user'
                                    ? 'bg-teal-600 text-white rounded-br-none'
                                    : 'bg-white text-gray-800 border border-gray-100 rounded-bl-none'
                                    }`}
                            >
                                {msg.role === 'user' ? (
                                    <div className="p-4">
                                        <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
                                    </div>
                                ) : (
                                    <div className="w-full">
                                        {(() => {
                                            try {
                                                // Try to parse content as JSON
                                                const data = JSON.parse(msg.content);
                                                return (
                                                    <div className="flex flex-col">
                                                        {/* Summary Header */}
                                                        <div className="bg-gradient-to-r from-teal-50 to-cyan-50 p-5 border-b border-teal-100">
                                                            <div className="flex items-start space-x-3">
                                                                <div className="p-2 bg-teal-100 rounded-lg">
                                                                    <svg className="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                                    </svg>
                                                                </div>
                                                                <div>
                                                                    <h4 className="font-semibold text-gray-900 mb-1">Health Insight</h4>
                                                                    <p className="text-gray-700 text-sm leading-relaxed">{data.summary}</p>
                                                                </div>
                                                            </div>
                                                        </div>

                                                        {/* Metrics Grid */}
                                                        {data.metrics && data.metrics.length > 0 && (
                                                            <div className="p-5 bg-white">
                                                                <h5 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Key Metrics</h5>
                                                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                                                    {data.metrics.map((metric, i) => (
                                                                        <div key={i} className="p-3 rounded-xl border border-gray-100 bg-gray-50 hover:border-teal-200 transition-colors">
                                                                            <div className="flex justify-between items-start mb-1">
                                                                                <span className="text-sm font-medium text-gray-600">{metric.label}</span>
                                                                                <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${metric.status === 'Normal' || metric.status === 'Good'
                                                                                    ? 'bg-green-100 text-green-700'
                                                                                    : metric.status === 'High' || metric.status === 'Low'
                                                                                        ? 'bg-amber-100 text-amber-700'
                                                                                        : 'bg-gray-100 text-gray-600'
                                                                                    }`}>
                                                                                    {metric.status}
                                                                                </span>
                                                                            </div>
                                                                            <div className="text-lg font-bold text-gray-900 mb-1">{metric.value}</div>
                                                                            <p className="text-xs text-gray-500 leading-snug">{metric.insight}</p>
                                                                        </div>
                                                                    ))}
                                                                </div>
                                                            </div>
                                                        )}

                                                        {/* Analysis & Recommendations */}
                                                        <div className="p-5 pt-0">
                                                            {data.analysis && (
                                                                <div className="mb-4">
                                                                    <h5 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Detailed Analysis</h5>
                                                                    <div className="space-y-3">
                                                                        {data.analysis.split('\n').filter(line => line.trim()).map((line, i) => {
                                                                            // Handle headings (### )
                                                                            if (line.startsWith('### ')) {
                                                                                return (
                                                                                    <h6 key={i} className="text-base font-bold text-teal-700 mt-4 mb-2 flex items-center">
                                                                                        <span className="w-1 h-5 bg-teal-500 mr-2 rounded"></span>
                                                                                        {line.replace('### ', '')}
                                                                                    </h6>
                                                                                );
                                                                            }

                                                                            // Handle bullet points (- )
                                                                            if (line.trim().startsWith('- **')) {
                                                                                const match = line.match(/- \*\*(.*?)\*\*:?\s*(.*)/);
                                                                                if (match) {
                                                                                    return (
                                                                                        <div key={i} className="flex items-start ml-4 mb-2">
                                                                                            <span className="w-1.5 h-1.5 bg-teal-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                                                                                            <div className="flex-1">
                                                                                                <span className="font-semibold text-gray-800">{match[1]}:</span>
                                                                                                <span className="text-gray-700 ml-1">{match[2]}</span>
                                                                                            </div>
                                                                                        </div>
                                                                                    );
                                                                                }
                                                                            }

                                                                            if (line.trim().startsWith('- ')) {
                                                                                return (
                                                                                    <div key={i} className="flex items-start ml-4 mb-2">
                                                                                        <span className="w-1.5 h-1.5 bg-gray-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                                                                                        <span className="text-sm text-gray-700">{line.replace('- ', '')}</span>
                                                                                    </div>
                                                                                );
                                                                            }

                                                                            // Handle bold text in regular paragraphs
                                                                            const renderWithBold = (text) => {
                                                                                const parts = text.split(/(\*\*.*?\*\*)/g);
                                                                                return parts.map((part, idx) => {
                                                                                    if (part.startsWith('**') && part.endsWith('**')) {
                                                                                        return <strong key={idx} className="font-semibold text-gray-900">{part.slice(2, -2)}</strong>;
                                                                                    }
                                                                                    return <span key={idx}>{part}</span>;
                                                                                });
                                                                            };

                                                                            return (
                                                                                <p key={i} className="text-sm text-gray-700 leading-relaxed">
                                                                                    {renderWithBold(line)}
                                                                                </p>
                                                                            );
                                                                        })}
                                                                    </div>
                                                                </div>
                                                            )}

                                                            {data.recommendations && data.recommendations.length > 0 && (
                                                                <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-4 border border-indigo-200">
                                                                    <h5 className="text-xs font-bold text-indigo-800 uppercase tracking-wider mb-3 flex items-center">
                                                                        <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                                                                        </svg>
                                                                        Recommendations
                                                                    </h5>
                                                                    <ul className="space-y-2.5">
                                                                        {data.recommendations.map((rec, i) => (
                                                                            <li key={i} className="flex items-start">
                                                                                <div className="flex-shrink-0 w-6 h-6 bg-indigo-500 rounded-full flex items-center justify-center text-white text-xs font-bold mt-0.5">
                                                                                    {i + 1}
                                                                                </div>
                                                                                <span className="ml-3 text-sm text-indigo-900 leading-relaxed">{rec}</span>
                                                                            </li>
                                                                        ))}
                                                                    </ul>
                                                                </div>
                                                            )}
                                                        </div>
                                                    </div>
                                                );
                                            } catch (e) {
                                                // Fallback for plain text messages
                                                return (
                                                    <div className="p-4">
                                                        <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
                                                    </div>
                                                );
                                            }
                                        })()}
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="flex justify-start">
                            <div className="bg-white p-4 rounded-2xl rounded-bl-none shadow-sm border border-gray-100">
                                <div className="flex space-x-2">
                                    <div className="w-2 h-2 bg-teal-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                    <div className="w-2 h-2 bg-teal-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                    <div className="w-2 h-2 bg-teal-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 bg-white border-t border-gray-100">
                    <form onSubmit={handleSendMessage} className="flex space-x-2">
                        <input
                            type="text"
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            placeholder="Ask about your health, sleep, or medications..."
                            className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-100 outline-none transition-all placeholder-gray-400"
                            disabled={isLoading}
                        />
                        <button
                            type="submit"
                            disabled={!inputText.trim() || isLoading}
                            className="bg-gradient-to-r from-teal-600 to-cyan-500 text-white px-6 py-3 rounded-xl font-medium hover:shadow-lg transform hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                        >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                            </svg>
                        </button>
                    </form>
                </div>
            </div>
        </Resizable >
    );
};

export default HealthChat;
