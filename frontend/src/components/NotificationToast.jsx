import React, { useEffect } from 'react';
import StarRating from '../features/reviews/StarRating';

const NotificationToast = ({ notification, onClose }) => {
    useEffect(() => {
        // Auto-dismiss after 5 seconds
        const timer = setTimeout(() => {
            onClose();
        }, 5000);

        return () => clearTimeout(timer);
    }, [onClose]);

    if (!notification) return null;

    return (
        <div className="fixed top-4 right-4 z-50 animate-slide-in-right">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700 p-4 max-w-sm">
                <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center space-x-2">
                        <div className="w-10 h-10 bg-yellow-100 dark:bg-yellow-900/30 rounded-full flex items-center justify-center">
                            <svg className="w-6 h-6 text-yellow-600 dark:text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                        </div>
                        <div>
                            <h4 className="font-semibold text-gray-900 dark:text-white">New Review!</h4>
                            <p className="text-xs text-gray-500 dark:text-gray-400">Just now</p>
                        </div>
                    </div>
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <div className="space-y-2">
                    <p className="text-sm text-gray-700 dark:text-gray-300">
                        <span className="font-medium">{notification.patient_name}</span> left you a review
                    </p>
                    <div className="flex items-center space-x-2">
                        <StarRating rating={notification.rating} size="sm" />
                        <span className="text-sm font-medium text-gray-900 dark:text-white">
                            {notification.rating}/5
                        </span>
                    </div>
                    {notification.comment && (
                        <p className="text-sm text-gray-600 dark:text-gray-400 italic line-clamp-2">
                            "{notification.comment}"
                        </p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default NotificationToast;
