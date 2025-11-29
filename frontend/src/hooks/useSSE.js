import { useEffect, useRef, useState } from 'react';

/**
 * Custom hook to manage Server-Sent Events (SSE) connection
 * @param {string} url - The SSE endpoint URL
 * @param {function} onMessage - Callback function to handle incoming messages
 * @param {boolean} enabled - Whether the connection should be active
 */
const useSSE = (url, onMessage, enabled = true) => {
    const [isConnected, setIsConnected] = useState(false);
    const eventSourceRef = useRef(null);
    const reconnectTimeoutRef = useRef(null);

    useEffect(() => {
        if (!enabled || !url) {
            return;
        }

        const connect = () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    console.warn('No auth token found for SSE connection');
                    return;
                }

                // Create EventSource with auth token in URL (since EventSource doesn't support headers)
                const eventSource = new EventSource(`${url}?token=${token}`);
                eventSourceRef.current = eventSource;

                eventSource.onopen = () => {
                    console.log('✅ SSE connection established');
                    setIsConnected(true);
                };

                eventSource.addEventListener('connected', (event) => {
                    console.log('📡 SSE connected event:', event.data);
                });

                eventSource.addEventListener('heartbeat', (event) => {
                    // Silent heartbeat to keep connection alive
                });

                eventSource.addEventListener('new_review', (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        console.log('⭐ New review received:', data);
                        if (onMessage) {
                            onMessage({ type: 'new_review', data });
                        }
                    } catch (error) {
                        console.error('Error parsing SSE message:', error);
                    }
                });

                eventSource.onerror = (error) => {
                    console.error('❌ SSE connection error:', error);
                    setIsConnected(false);
                    eventSource.close();

                    // Attempt to reconnect after 5 seconds
                    reconnectTimeoutRef.current = setTimeout(() => {
                        console.log('🔄 Attempting to reconnect SSE...');
                        connect();
                    }, 5000);
                };

            } catch (error) {
                console.error('Error creating SSE connection:', error);
            }
        };

        connect();

        // Cleanup function
        return () => {
            if (eventSourceRef.current) {
                eventSourceRef.current.close();
                eventSourceRef.current = null;
            }
            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current);
            }
            setIsConnected(false);
        };
    }, [url, enabled, onMessage]);

    return { isConnected };
};

export default useSSE;
