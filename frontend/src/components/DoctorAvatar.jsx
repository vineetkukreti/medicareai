import React from 'react';

const DoctorAvatar = ({ image, name, size = "md", className = "" }) => {
    const getSizeClasses = () => {
        switch (size) {
            case "sm": return "h-8 w-8 text-xs";
            case "md": return "h-12 w-12 text-lg";
            case "lg": return "h-16 w-16 text-2xl";
            case "xl": return "h-24 w-24 text-4xl";
            default: return "h-12 w-12 text-lg";
        }
    };

    if (image) {
        return (
            <img
                src={image}
                alt={name}
                className={`rounded-full object-cover border border-gray-200 dark:border-gray-600 ${getSizeClasses()} ${className}`}
            />
        );
    }

    return (
        <div className={`rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold ${getSizeClasses()} ${className}`}>
            {name ? name[0].toUpperCase() : 'D'}
        </div>
    );
};

export default DoctorAvatar;
