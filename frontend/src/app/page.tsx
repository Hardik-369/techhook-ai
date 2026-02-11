import React from 'react';
import { LayoutDashboard, Settings, Activity, Youtube, Linkedin, Image as ImageIcon } from 'lucide-react';

export default function Dashboard() {
    return (
        <main className="max-w-7xl mx-auto p-6 space-y-8">
            {/* Header */}
            <div className="flex justify-between items-center border-b border-slate-800 pb-6">
                <div>
                    <h1 className="text-4xl font-black bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
                        TechHook AI
                    </h1>
                    <p className="text-slate-400 mt-1">Creator-to-LinkedIn Amplifier</p>
                </div>
                <div className="flex gap-4">
                    <button className="flex items-center gap-2 bg-slate-900 border border-slate-700 px-4 py-2 rounded-xl hover:bg-slate-800 transition">
                        <Activity className="w-4 h-4 text-green-400" />
                        <span>Automation: ON</span>
                    </button>
                    <button className="bg-blue-600 hover:bg-blue-500 px-6 py-2 rounded-xl font-bold transition">
                        Post Now
                    </button>
                </div>
            </div>

            {/* Hero Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                    { label: 'Total Posts', value: '42', icon: Linkedin, color: 'text-blue-400' },
                    { label: 'Total Views', value: '1.2M', icon: Activity, color: 'text-green-400' },
                    { label: 'Videos Processed', value: '12', icon: Youtube, color: 'text-red-400' },
                ].map((stat, i) => (
                    <div key={i} className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl flex items-center gap-4">
                        <div className={`p-4 rounded-xl bg-slate-900 ${stat.color}`}>
                            <stat.icon className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-slate-400 text-sm font-medium">{stat.label}</p>
                            <p className="text-2xl font-bold">{stat.value}</p>
                        </div>
                    </div>
                ))}
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Preview Section */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="bg-slate-900/50 border border-slate-800 rounded-2xl overflow-hidden p-6">
                        <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                            <Activity className="w-5 h-5 text-blue-400" />
                            Latest Generated Post
                        </h2>

                        <div className="space-y-4">
                            <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 text-slate-300 leading-relaxed font-mono text-sm">
                                <p className="font-bold text-white mb-4">AI Is Replacing Smart Founders...</p>
                                <p>If you're still building like it's 2023, you're already behind.</p>
                                <p>The smartest founders aren't hiring more people.</p>
                                <p>They're building AI agents to replace workflows.</p>
                                <p className="mt-4">#AI #Founders #Automation #TechHook #FutureOfWork</p>
                            </div>

                            <div className="relative aspect-square w-full max-w-sm mx-auto bg-slate-950 border border-slate-800 rounded-xl overflow-hidden group">
                                <div className="absolute inset-0 bg-gradient-to-br from-blue-900 to-slate-950 flex items-center justify-center p-8 text-center">
                                    <p className="text-2xl font-black text-white">AI IS REPLACING SMART FOUNDERS</p>
                                </div>
                                <div className="absolute top-4 right-4 bg-black/50 backdrop-blur-md p-2 rounded-lg text-xs font-bold">
                                    Generated hook image
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Status/Logs Section */}
                <div className="space-y-6">
                    <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 h-full">
                        <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                            <Activity className="w-5 h-5 text-purple-400" />
                            Live Logs
                        </h2>
                        <div className="space-y-4 font-mono text-sm">
                            {[
                                { time: '10:45 AM', msg: 'Checking RSS Feed...', status: 'success' },
                                { time: '10:46 AM', msg: 'New Video: AI Agents Explained', status: 'success' },
                                { time: '10:47 AM', msg: 'Extracting Transcript (1,200 words)', status: 'success' },
                                { time: '10:48 AM', msg: 'Generating LinkedIn Post...', status: 'loading' },
                            ].map((log, i) => (
                                <div key={i} className="flex gap-3 text-slate-400">
                                    <span className="text-slate-600">{log.time}</span>
                                    <span className={log.status === 'success' ? 'text-green-400' : 'text-blue-400'}>
                                        {log.msg}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
}
