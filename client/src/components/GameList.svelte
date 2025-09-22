<script lang="ts">
    import { onMount } from "svelte";

    interface Game {
        id: number;
        title: string;
        description: string;
        publisher_name?: string;
        category_name?: string;
    }

    export let games: Game[] = [];
    let loading = true;
    let error: string | null = null;

    const fetchGames = async () => {
        loading = true;
        try {
            const response = await fetch('/api/games');
            if(response.ok) {
                games = await response.json();
            } else {
                error = `Failed to fetch data: ${response.status} ${response.statusText}`;
            }
        } catch (err) {
            error = `Error: ${err instanceof Error ? err.message : String(err)}`;
        } finally {
            loading = false;
        }
    };

    onMount(() => {
        fetchGames();
    });
</script>

<div class="relative">
    <!-- Section Header -->
    <div class="text-center mb-12">
        <h2 class="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent">
            Featured Games
        </h2>
        <p class="text-lg text-slate-400 max-w-2xl mx-auto">
            Discover innovative board games crafted by developers, for developers. 
            Each game brings coding concepts to life in unique and engaging ways.
        </p>
        <div class="mt-6 w-24 h-1 bg-gradient-to-r from-blue-500 to-purple-500 mx-auto rounded-full"></div>
    </div>
    
    {#if loading}
        <!-- Enhanced loading animation -->
        <div class="text-center py-16">
            <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full mb-4 animate-spin">
                <div class="w-12 h-12 border-4 border-white/30 border-t-white rounded-full"></div>
            </div>
            <p class="text-slate-400 text-lg">Loading amazing games...</p>
        </div>
        
        <!-- Enhanced loading skeleton -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {#each Array(6) as _, i}
                <div class="group bg-slate-800/40 backdrop-blur-sm rounded-2xl overflow-hidden shadow-lg border border-slate-700/30 animate-pulse">
                    <div class="p-8">
                        <div class="space-y-4">
                            <div class="h-7 bg-gradient-to-r from-slate-700 to-slate-600 rounded-lg w-3/4"></div>
                            <div class="space-y-2">
                                <div class="h-4 bg-slate-700 rounded w-full"></div>
                                <div class="h-4 bg-slate-700 rounded w-4/5"></div>
                                <div class="h-4 bg-slate-700 rounded w-3/5"></div>
                            </div>
                            <div class="flex gap-2 pt-2">
                                <div class="h-6 bg-slate-700 rounded-full w-20"></div>
                                <div class="h-6 bg-slate-700 rounded-full w-16"></div>
                            </div>
                            <div class="h-10 bg-gradient-to-r from-slate-700 to-slate-600 rounded-lg w-32 mt-6"></div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else if error}
        <!-- Enhanced error display -->
        <div class="text-center py-16">
            <div class="bg-red-500/10 border border-red-500/20 rounded-2xl p-8 max-w-md mx-auto">
                <div class="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-semibold text-red-400 mb-2">Oops! Something went wrong</h3>
                <p class="text-red-300/80">{error}</p>
                <button 
                    on:click={fetchGames}
                    class="mt-4 px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors duration-300"
                >
                    Try Again
                </button>
            </div>
        </div>
    {:else if games.length === 0}
        <!-- Enhanced empty state -->
        <div class="text-center py-16">
            <div class="w-24 h-24 bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg class="w-12 h-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
                </svg>
            </div>
            <h3 class="text-2xl font-semibold text-slate-300 mb-2">No Games Found</h3>
            <p class="text-slate-400">Check back soon for exciting new games!</p>
        </div>
    {:else}
        <!-- Enhanced games grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8" data-testid="games-grid">
            {#each games as game, index (game.id)}
                <a
                    href="/game/{game.id}"
                    class="group block bg-slate-800/30 backdrop-blur-sm rounded-2xl overflow-hidden shadow-lg border border-slate-700/30 hover:border-blue-500/40 hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-500 hover:scale-[1.02] hover:-translate-y-2 transform-gpu"
                    data-testid="game-card"
                    data-game-id={game.id}
                    data-game-title={game.title}
                    style="animation-delay: {index * 0.1}s"
                >
                    <!-- Card content -->
                    <div class="p-8 relative overflow-hidden">
                        <!-- Background gradient overlay -->
                        <div class="absolute inset-0 bg-gradient-to-br from-blue-600/5 via-purple-600/5 to-indigo-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                        
                        <!-- Animated background elements -->
                        <div class="absolute -top-4 -right-4 w-24 h-24 bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-full blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 group-hover:animate-pulse"></div>
                        
                        <div class="relative z-10">
                            <!-- Title -->
                            <h3 class="text-2xl font-bold text-slate-100 mb-4 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-purple-400 group-hover:bg-clip-text transition-all duration-300" data-testid="game-title">
                                {game.title}
                            </h3>
                            
                            <!-- Tags -->
                            {#if game.category_name || game.publisher_name}
                                <div class="flex flex-wrap gap-2 mb-4">
                                    {#if game.category_name}
                                        <span class="px-3 py-1 bg-blue-500/20 text-blue-300 text-sm rounded-full border border-blue-500/30 group-hover:bg-blue-500/30 group-hover:border-blue-400/50 transition-all duration-300" data-testid="game-category">
                                            {game.category_name}
                                        </span>
                                    {/if}
                                    {#if game.publisher_name}
                                        <span class="px-3 py-1 bg-purple-500/20 text-purple-300 text-sm rounded-full border border-purple-500/30 group-hover:bg-purple-500/30 group-hover:border-purple-400/50 transition-all duration-300" data-testid="game-publisher">
                                            {game.publisher_name}
                                        </span>
                                    {/if}
                                </div>
                            {/if}
                            
                            <!-- Description -->
                            <p class="text-slate-300 mb-6 leading-relaxed group-hover:text-slate-200 transition-colors duration-300 line-clamp-4" data-testid="game-description">
                                {game.description}
                            </p>
                            
                            <!-- Progress bar (mock funding progress) -->
                            <div class="mb-6">
                                <div class="flex justify-between text-sm text-slate-400 mb-2">
                                    <span>Funding Progress</span>
                                    <span>{Math.floor(Math.random() * 100)}%</span>
                                </div>
                                <div class="w-full bg-slate-700/50 rounded-full h-2 overflow-hidden">
                                    <div 
                                        class="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full transition-all duration-1000 group-hover:from-blue-400 group-hover:to-purple-400"
                                        style="width: {Math.floor(Math.random() * 100)}%"
                                    ></div>
                                </div>
                            </div>
                            
                            <!-- Call to action -->
                            <div class="flex items-center justify-between">
                                <div class="flex items-center text-blue-400 font-semibold group-hover:text-blue-300 transition-colors duration-300">
                                    <span class="mr-2">View details</span>
                                    <svg class="w-5 h-5 transform group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                                    </svg>
                                </div>
                                
                                <!-- Mock funding amount -->
                                <div class="text-right">
                                    <div class="text-lg font-bold text-slate-200 group-hover:text-white transition-colors duration-300">
                                        ${Math.floor(Math.random() * 50000) + 10000}
                                    </div>
                                    <div class="text-xs text-slate-500">raised</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
        
        <!-- Call to action section -->
        <div class="text-center mt-16 py-12 px-6 bg-gradient-to-r from-blue-900/20 to-purple-900/20 rounded-2xl border border-slate-700/30 backdrop-blur-sm">
            <h3 class="text-2xl font-bold text-slate-200 mb-4">Ready to back a project?</h3>
            <p class="text-slate-400 mb-6 max-w-md mx-auto">Join thousands of developers supporting innovative gaming experiences.</p>
            <button class="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-blue-500/25 transition-all duration-300 hover:scale-105">
                Start Supporting
            </button>
        </div>
    {/if}
</div>

<style>
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .grid > * {
        animation: slideInUp 0.6s ease-out both;
    }
    
    .line-clamp-4 {
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
</style>