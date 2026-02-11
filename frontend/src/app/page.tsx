'use client';
import React, { useEffect, useState } from 'react';
import { LayoutDashboard, Settings, Activity, Youtube, Linkedin, Image as ImageIcon, Loader2 } from 'lucide-react';

const RAW_URL = "https://raw.githubusercontent.com/Hardik-369/techhook-ai/main/backend/data";

interface Log {
    time: string;
    msg: string;
    status: 'success' | 'error' | 'loading';
}

interface Store {
    processed_ids: string[];
}

export default function Dashboard() {
    const [logs, setLogs] = useState<Log[]>([]);
    const [store, setStore] = useState<Store>({ processed_ids: [] });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchData() {
            try {
                const [logsRes, storeRes] = await Promise.all([
                    fetch(`${RAW_URL}/logs.json?t=${Date.now()}`),
                    fetch(`${RAW_URL}/store.json?t=${Date.now()}`)
                ]);

                if (logsRes.ok) setLogs(await logsRes.json());
                if (storeRes.ok) setStore(await storeRes.json());
            } catch (error) {
                console.error("Failed to fetch dashboard data:", error);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
        const interval = setInterval(fetchData, 60000); // Refresh every minute
        return () => clearInterval(interval);
    }, []);

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
                    <div className="flex items-center gap-2 bg-slate-900 border border-slate-700 px-4 py-2 rounded-xl">
                        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                        <span className="text-sm font-medium">System Active</span>
                    </div>
                    <button className="bg-blue-600 hover:bg-blue-500 px-6 py-2 rounded-xl font-bold transition">
                        Force Check
                    </button>
                </div>
            </div>

            {/* Hero Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                    { label: 'Total Posts', value: store.processed_ids.length, icon: Linkedin, color: 'text-blue-400' },
                    { label: 'Videos Processed', value: store.processed_ids.length, icon: Youtube, color: 'text-red-400' },
                    { label: 'System Uptime', value: '99.9%', icon: Activity, color: 'text-green-400' },
                ].map((stat, i) => (
                    <div key={i} className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl flex items-center gap-4 hover:border-slate-700 transition">
                        <div className={`p-4 rounded-xl bg-slate-950 ${stat.color}`}>
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
                {/* Logs Section */}
                <div className="lg:col-span-1 space-y-6">
                    <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 h-full flex flex-col">
                        <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                            <Activity className="w-5 h-5 text-purple-400" />
                            Recent Activity
                        </h2>
                        <div className="flex-1 space-y-4 font-mono text-sm overflow-y-auto max-h-[600px] pr-2 custom-scrollbar">
                            {loading && logs.length === 0 ? (
                                <div className="flex items-center gap-2 text-slate-500">
                                    <Loader2 className="w-4 h-4 animate-spin" />
                                    Initial sync...
                                </div>
                            ) : logs.length > 0 ? (
                                logs.map((log, i) => (
                                    <div key={i} className="flex flex-col gap-1 border-l-2 border-slate-800 pl-4 py-1 hover:border-slate-600 transition">
                                        <span className="text-slate-600 text-xs">{log.time}</span>
                                        <span className={log.status === 'success' ? 'text-slate-200' : 'text-red-400'}>
                                            {log.msg}
                                        </span>
                                    </div>
                                ))
                            ) : (
                                <p className="text-slate-500 italic text-center py-10">No logs found yet.</p>
                            )}
                        </div>
                    </div>
                </div>

                {/* Status/Preview Section */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
                        <h2 className="text-xl font-bold mb-6 flex items-center gap-2 text-blue-400">
                            <ImageIcon className="w-5 h-5" />
                            Latest Visual Asset
                        </h2>

                        {store.processed_ids.length > 0 ? (
                            <div className="space-y-6">
                                <div className="relative aspect-square w-full max-w-md mx-auto bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden group shadow-2xl">
                                    {/* eslint-disable-next-line @next/next/no-img-element */}
                                    <img
                                        src={`${RAW_URL}/${store.processed_ids[store.processed_ids.length - 1]}.png`}
                                        alt="Latest generated post hook"
                                        className="w-full h-full object-cover grayscale-[0.2] group-hover:grayscale-0 transition duration-500"
                                        onError={(e) => {
                                            e.currentTarget.src = "https://placehold.co/1080x1080/020617/ffffff?text=Generating+Image...";
                                        }}
                                    />
                                    <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/80 to-transparent p-6 translate-y-2 group-hover:translate-y-0 transition duration-300">
                                        <p className="text-xs text-blue-400 font-bold tracking-widest uppercase mb-1">Visual ID</p>
                                        <p className="text-sm font-mono text-white opacity-60 truncate">{store.processed_ids[store.processed_ids.length - 1]}</p>
                                    </div>
                                </div>

                                <div className="bg-slate-950/50 border border-dashed border-slate-800 rounded-xl p-4 text-center">
                                    <p className="text-slate-400 text-sm">
                                        Image is automatically pushed to GitHub and served via CDN.
                                    </p>
                                </div>
                            </div>
                        ) : (
                            <div className="aspect-square w-full max-w-sm mx-auto flex flex-col items-center justify-center border-2 border-dashed border-slate-800 rounded-3xl p-10 text-center text-slate-500 gap-4">
                                <Loader2 className="w-10 h-10 animate-spin opacity-20" />
                                <p className="font-medium animate-pulse">Waiting for first automated run...</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </main>
    );
}
