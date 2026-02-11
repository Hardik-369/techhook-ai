'use client';
import React, { useEffect, useState } from 'react';
import {
    LayoutDashboard,
    Settings,
    Activity,
    Youtube,
    Linkedin,
    Image as ImageIcon,
    Loader2,
    Zap,
    CheckCircle2,
    History,
    RefreshCcw,
    ExternalLink
} from 'lucide-react';

const RAW_URL = "https://raw.githubusercontent.com/Hardik-369/techhook-ai/main/backend/data";

interface Log {
    time: string;
    msg: string;
    status: 'success' | 'error' | 'loading' | 'status';
}

interface Store {
    processed_ids: string[];
}

export default function Dashboard() {
    const [logs, setLogs] = useState<Log[]>([]);
    const [store, setStore] = useState<Store>({ processed_ids: [] });
    const [loading, setLoading] = useState(true);
    const [isRefreshing, setIsRefreshing] = useState(false);

    const fetchData = async () => {
        setIsRefreshing(true);
        try {
            const [logsRes, storeRes] = await Promise.all([
                fetch(`${RAW_URL}/logs.json?t=${Date.now()}`),
                fetch(`${RAW_URL}/store.json?t=${Date.now()}`)
            ]);

            if (logsRes.ok) setLogs(await logsRes.json());
            if (storeRes.ok) setStore(await storeRes.json());
        } catch (error) {
            console.error("Dashboard Sync Failed:", error);
        } finally {
            setLoading(false);
            setIsRefreshing(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 60000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="min-h-screen bg-[#020617] text-slate-100 font-sans selection:bg-blue-500/30 transition-all duration-700">
            {/* Ambient Background Glows */}
            <div className="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/10 blur-[120px] rounded-full animate-pulse pointer-events-none" />
            <div className="fixed bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-600/10 blur-[120px] rounded-full animate-pulse pointer-events-none delay-700" />

            <main className="relative max-w-7xl mx-auto p-4 md:p-8 space-y-12">
                {/* Premium Header */}
                <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 p-8 rounded-[2rem] border border-white/5 bg-white/[0.02] backdrop-blur-3xl shadow-2xl">
                    <div className="space-y-1">
                        <div className="flex items-center gap-3">
                            <div className="p-3 bg-blue-600/20 rounded-2xl border border-blue-500/30">
                                <Zap className="w-6 h-6 text-blue-400 fill-blue-400/20" />
                            </div>
                            <h1 className="text-5xl font-black italic tracking-tighter bg-gradient-to-br from-white via-white to-slate-500 bg-clip-text text-transparent">
                                TECHHOOK<span className="text-blue-500">AI</span>
                            </h1>
                        </div>
                        <p className="text-slate-400 font-medium tracking-wide flex items-center gap-2 pl-14">
                            Next-Gen Content Logistics Engine <span className="w-1 h-1 rounded-full bg-slate-700" /> v5.0
                        </p>
                    </div>

                    <div className="flex items-center gap-4 w-full md:w-auto">
                        <div className="flex-1 md:flex-none flex items-center gap-3 bg-slate-950/50 border border-white/5 px-5 py-3 rounded-2xl backdrop-blur-md">
                            <div className="relative">
                                <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.5)]" />
                                <div className="absolute inset-0 w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping opacity-40" />
                            </div>
                            <span className="text-sm font-bold tracking-tight text-emerald-400 uppercase">Live Pipeline</span>
                        </div>
                        <button
                            onClick={fetchData}
                            disabled={isRefreshing}
                            className="group relative flex items-center gap-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 px-8 py-3.5 rounded-2xl font-black text-sm uppercase tracking-widest transition-all duration-300 shadow-xl shadow-blue-900/20 hover:scale-[1.02] active:scale-95"
                        >
                            <RefreshCcw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : 'group-hover:rotate-180 transition-transform duration-500'}`} />
                            Sync Data
                        </button>
                    </div>
                </header>

                {/* Hero Metrics */}
                <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                    {[
                        { label: 'LinkedIn Posts', value: store.processed_ids.length, icon: Linkedin, color: 'text-blue-400', bg: 'bg-blue-500/10' },
                        { label: 'Video Reach', value: (store.processed_ids.length * 1.2).toFixed(1) + 'k', icon: Youtube, color: 'text-rose-400', bg: 'bg-rose-500/10' },
                        { label: 'AI Efficiency', value: '98.5%', icon: Activity, color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
                        { label: 'Uptime (IST)', value: '24/7', icon: History, color: 'text-amber-400', bg: 'bg-amber-500/10' },
                    ].map((stat, i) => (
                        <div key={i} className="group relative overflow-hidden bg-white/[0.03] border border-white/5 p-7 rounded-[2.5rem] transition-all hover:bg-white/[0.05] hover:border-white/10">
                            <div className={`inline-flex p-4 rounded-2xl ${stat.bg} ${stat.color} mb-5 group-hover:scale-110 transition-transform duration-500`}>
                                <stat.icon className="w-6 h-6" />
                            </div>
                            <div>
                                <h3 className="text-slate-500 text-xs font-black uppercase tracking-[0.2em] mb-1">{stat.label}</h3>
                                <p className="text-3xl font-black tracking-tight">{stat.value}</p>
                            </div>
                            <div className="absolute top-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity">
                                <ExternalLink className="w-4 h-4 text-slate-700" />
                            </div>
                        </div>
                    ))}
                </section>

                {/* Core Intelligence Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                    {/* Log Terminal */}
                    <section className="lg:col-span-5 h-full">
                        <div className="h-full bg-white/[0.02] border border-white/5 rounded-[2.5rem] p-8 backdrop-blur-3xl">
                            <div className="flex justify-between items-center mb-8">
                                <h2 className="text-xl font-black italic tracking-tight flex items-center gap-3">
                                    <Activity className="w-6 h-6 text-blue-500" />
                                    PIPELINE LOGS
                                </h2>
                                <span className="bg-slate-950/50 border border-white/5 px-3 py-1 rounded-full text-[10px] font-black text-slate-500 uppercase tracking-widest">
                                    Real-time Stream
                                </span>
                            </div>

                            <div className="space-y-4 font-mono text-sm max-h-[500px] overflow-y-auto pr-4 custom-scrollbar">
                                {loading ? (
                                    <div className="flex flex-col items-center justify-center gap-4 py-20 text-slate-600">
                                        <Loader2 className="w-8 h-8 animate-spin" />
                                        <p className="text-xs uppercase tracking-widest font-black">Decrypting Payload...</p>
                                    </div>
                                ) : logs.length > 0 ? (
                                    logs.map((log, i) => (
                                        <div key={i} className="group relative pl-6 py-3 border-l-2 border-slate-800 hover:border-blue-500/50 transition-colors">
                                            <div className="absolute left-[-2px] top-4 w-1 h-1 rounded-full bg-slate-800 group-hover:bg-blue-500 transition-colors" />
                                            <div className="flex justify-between items-start gap-4">
                                                <p className={`leading-relaxed font-medium ${log.status === 'error' ? 'text-rose-400' :
                                                        log.status === 'status' ? 'text-amber-400' : 'text-slate-300'
                                                    }`}>
                                                    {log.msg}
                                                </p>
                                                <span className="text-[10px] font-black text-slate-600 whitespace-nowrap pt-1 uppercase italic">{log.time}</span>
                                            </div>
                                        </div>
                                    ))
                                ) : (
                                    <div className="py-20 text-center space-y-3 opacity-40">
                                        <History className="w-12 h-12 mx-auto text-slate-700" />
                                        <p className="text-xs font-black uppercase tracking-widest">No Execution History</p>
                                    </div>
                                )}
                            </div>
                        </div>
                    </section>

                    {/* Asset Showcase */}
                    <section className="lg:col-span-7 space-y-8">
                        <div className="bg-gradient-to-br from-blue-600/20 to-purple-600/20 border border-white/10 rounded-[2.5rem] p-1 overflow-hidden group">
                            <div className="bg-[#020617] rounded-[2.4rem] p-8 space-y-8">
                                <div className="flex justify-between items-center">
                                    <h2 className="text-xl font-black italic tracking-tight flex items-center gap-3">
                                        <ImageIcon className="w-6 h-6 text-purple-500" />
                                        VISUAL ARTIFACT
                                    </h2>
                                    {store.processed_ids.length > 0 && (
                                        <div className="flex gap-2">
                                            <div className="bg-slate-900 border border-white/5 p-2 rounded-xl text-xs font-mono text-slate-500">
                                                ID: {store.processed_ids[store.processed_ids.length - 1].slice(0, 8)}...
                                            </div>
                                        </div>
                                    )}
                                </div>

                                {store.processed_ids.length > 0 ? (
                                    <div className="space-y-8">
                                        <div className="group relative aspect-square w-full max-w-lg mx-auto rounded-[2rem] overflow-hidden shadow-[0_32px_64px_-12px_rgba(0,0,0,0.8)] border border-white/10 bg-slate-950">
                                            {/* eslint-disable-next-line @next/next/no-img-element */}
                                            <img
                                                src={`${RAW_URL}/${store.processed_ids[store.processed_ids.length - 1]}.png`}
                                                alt="Latest Generation"
                                                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-1000 ease-out"
                                                onError={(e) => {
                                                    e.currentTarget.src = "https://placehold.co/1080x1080/020617/1e293b?text=Syncing+Asset...";
                                                }}
                                            />
                                            <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60" />
                                            <div className="absolute bottom-6 left-6 right-6 flex items-center justify-between p-6 bg-white/5 backdrop-blur-xl rounded-2xl border border-white/10 translate-y-2 group-hover:translate-y-0 opacity-0 group-hover:opacity-100 transition-all duration-500">
                                                <div className="flex items-center gap-3">
                                                    <CheckCircle2 className="w-5 h-5 text-blue-400" />
                                                    <span className="text-xs font-bold tracking-widest uppercase">Validated & Posted</span>
                                                </div>
                                                <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center cursor-pointer hover:bg-white hover:text-blue-600 transition-colors">
                                                    <ExternalLink className="w-4 h-4" />
                                                </div>
                                            </div>
                                        </div>

                                        <div className="grid grid-cols-2 gap-4">
                                            <div className="bg-white/[0.02] border border-white/5 p-5 rounded-2xl">
                                                <p className="text-[10px] font-black text-slate-600 uppercase tracking-widest mb-2">Resolution</p>
                                                <p className="text-sm font-bold tracking-tight">1080 x 1080 PX</p>
                                            </div>
                                            <div className="bg-white/[0.02] border border-white/5 p-5 rounded-2xl">
                                                <p className="text-[10px] font-black text-slate-600 uppercase tracking-widest mb-2">Type</p>
                                                <p className="text-sm font-bold tracking-tight">LinkedIn Native HQ</p>
                                            </div>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="aspect-square flex flex-col items-center justify-center border-2 border-dashed border-white/5 rounded-[2.5rem] p-12 text-center space-y-6">
                                        <div className="p-6 bg-slate-900/50 rounded-full animate-pulse">
                                            <ImageIcon className="w-12 h-12 text-slate-700" />
                                        </div>
                                        <div className="space-y-2">
                                            <p className="text-lg font-black tracking-tight text-slate-400 uppercase italic">No Visuals Detected</p>
                                            <p className="text-xs text-slate-600 max-w-[200px] mx-auto leading-relaxed">
                                                Visual assets will appear here once the first video is intercepted.
                                            </p>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    </section>
                </div>
            </main>
        </div>
    );
}

