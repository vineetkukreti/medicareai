import React from 'react';

const MarketInsight = () => {
    const marketData = [
        { id: 1, crop: 'Wheat', market: 'Delhi Mandi', price: '₹2100/quintal', trend: 'up' },
        { id: 2, crop: 'Rice', market: 'Karnal Mandi', price: '₹3500/quintal', trend: 'stable' },
        { id: 3, crop: 'Potato', market: 'Agra Mandi', price: '₹800/quintal', trend: 'down' },
        { id: 4, crop: 'Tomato', market: 'Nashik Mandi', price: '₹1200/quintal', trend: 'up' },
        { id: 5, crop: 'Onion', market: 'Lasalgaon Mandi', price: '₹1500/quintal', trend: 'up' },
    ];

    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
                <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Market Insights</h2>

                <div className="bg-white shadow-md rounded-lg overflow-hidden">
                    <div className="p-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Live Market Prices</h3>
                        <input
                            type="text"
                            placeholder="Search crop..."
                            className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-1 focus:ring-green-500"
                        />
                    </div>
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Crop</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Market</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trend</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {marketData.map((item) => (
                                <tr key={item.id}>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{item.crop}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.market}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-bold">{item.price}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                                        {item.trend === 'up' && <span className="text-green-600 flex items-center">▲ Up</span>}
                                        {item.trend === 'down' && <span className="text-red-600 flex items-center">▼ Down</span>}
                                        {item.trend === 'stable' && <span className="text-gray-600 flex items-center">● Stable</span>}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default MarketInsight;
