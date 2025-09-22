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

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Section Header -->
    <div class="text-center mb-12">
        <h2 class="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-blue-300 bg-clip-text text-transparent mb-4">
            Featured Games
        </h2>
        <p class="text-xl text-slate-400 max-w-2xl mx-auto">
            Discover innovative DevOps-themed board games that challenge your strategic thinking
        </p>
        <div class="w-24 h-1 bg-gradient-to-r from-blue-500 to-purple-500 mx-auto mt-6 rounded-full"></div>
    </div>
    
    {#if loading}
        <!-- Enhanced loading animation -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {#each Array(8) as _, i}
                <div class="group relative overflow-hidden bg-slate-800/40 backdrop-blur-sm rounded-2xl border border-slate-700/50 shadow-xl">
                    <div class="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5"></div>
                    <div class="relative p-6">
                        <div class="animate-pulse space-y-4">
                            <!-- Shimmer effect -->
                            <div class="absolute inset-0 -translate-x-full animate-[shimmer_2s_infinite] bg-gradient-to-r from-transparent via-white/5 to-transparent"></div>
                            
                            <div class="h-6 bg-slate-700/60 rounded-lg w-3/4"></div>
                            <div class="flex space-x-2">
                                <div class="h-6 bg-slate-700/60 rounded-full w-16"></div>
                                <div class="h-6 bg-slate-700/60 rounded-full w-20"></div>
                            </div>
                            <div class="space-y-2">
                                <div class="h-4 bg-slate-700/60 rounded w-full"></div>
                                <div class="h-4 bg-slate-700/60 rounded w-5/6"></div>
                                <div class="h-4 bg-slate-700/60 rounded w-4/6"></div>
                            </div>
                            <div class="h-10 bg-slate-700/60 rounded-lg w-full mt-6"></div>
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
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                </div>
                <h3 class="text-lg font-semibold text-red-400 mb-2">Oops! Something went wrong</h3>
                <p class="text-red-300/80 text-sm">{error}</p>
                <button 
                    on:click={fetchGames}
                    class="mt-4 bg-red-600 hover:bg-red-500 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200"
                >
                    Try Again
                </button>
            </div>
        </div>
    {:else if games.length === 0}
        <!-- Enhanced empty state -->
        <div class="text-center py-16">
            <div class="bg-slate-800/40 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8 max-w-md mx-auto">
                <div class="w-16 h-16 bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                    </svg>
                </div>
                <h3 class="text-lg font-semibold text-slate-300 mb-2">No games available</h3>
                <p class="text-slate-400 text-sm">Check back soon for exciting new games!</p>
            </div>
        </div>
    {:else}
        <!-- Enhanced game cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6" data-testid="games-grid">
            {#each games as game, index (game.id)}
                <a 
                    href={`/game/${game.id}`} 
                    class="group block relative overflow-hidden bg-slate-800/40 backdrop-blur-sm rounded-2xl border border-slate-700/50 hover:border-blue-500/50 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-500 transform hover:scale-[1.02] hover:-translate-y-2"
                    data-testid="game-card"
                    data-game-id={game.id}
                    data-game-title={game.title}
                    style="animation-delay: {index * 100}ms"
                >
                    <!-- Background gradient overlay -->
                    <div class="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/5 to-indigo-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                    
                    <!-- Animated border gradient -->
                    <div class="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-blue-500/20 p-[1px]">
                        <div class="w-full h-full bg-slate-800/40 backdrop-blur-sm rounded-2xl"></div>
                    </div>

                    <div class="relative p-6 z-10">
                        <!-- Game Title -->
                        <h3 class="text-xl font-bold text-slate-100 mb-3 group-hover:text-blue-300 transition-colors duration-300 line-clamp-2" data-testid="game-title">
                            {game.title}
                        </h3>
                        
                        <!-- Tags -->
                        {#if game.category_name || game.publisher_name}
                            <div class="flex flex-wrap gap-2 mb-4">
                                {#if game.category_name}
                                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-500/20 text-blue-300 border border-blue-500/30 group-hover:bg-blue-500/30 transition-colors duration-300" data-testid="game-category">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                                        </svg>
                                        {game.category_name}
                                    </span>
                                {/if}
                                {#if game.publisher_name}
                                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-500/20 text-purple-300 border border-purple-500/30 group-hover:bg-purple-500/30 transition-colors duration-300" data-testid="game-publisher">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                        </svg>
                                        {game.publisher_name}
                                    </span>
                                {/if}
                            </div>
                        {/if}
                        
                        <!-- Description -->
                        <p class="text-slate-400 mb-6 text-sm leading-relaxed line-clamp-3 group-hover:text-slate-300 transition-colors duration-300" data-testid="game-description">
                            {game.description}
                        </p>
                        
                        <!-- CTA Button -->
                        <div class="flex items-center justify-between pt-4 border-t border-slate-700/50 group-hover:border-slate-600/50 transition-colors duration-300">
                            <div class="flex items-center text-sm font-medium text-blue-400 group-hover:text-blue-300 transition-colors duration-300">
                                <span>View Details</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-2 transform transition-transform duration-300 group-hover:translate-x-2" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                            </div>
                            
                            <!-- Funding progress indicator (placeholder) -->
                            <div class="flex items-center space-x-1">
                                <div class="w-2 h-2 bg-green-500/60 rounded-full animate-pulse"></div>
                                <span class="text-xs text-slate-500 group-hover:text-slate-400 transition-colors duration-300">Active</span>
                            </div>
                        </div>
                    </div>

                    <!-- Hover glow effect -->
                    <div class="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none">
                        <div class="absolute inset-0 rounded-2xl bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-blue-500/10 blur-xl"></div>
                    </div>
                </a>
            {/each}
        </div>

        <!-- Load more button -->
        {#if games.length >= 12}
            <div class="text-center mt-12">
                <button class="group bg-slate-800/60 hover:bg-slate-800/80 backdrop-blur-sm border border-slate-700/50 hover:border-slate-600/50 text-slate-300 hover:text-white font-medium py-3 px-8 rounded-xl transition-all duration-300 transform hover:scale-105">
                    <span class="flex items-center space-x-2">
                        <span>Load More Games</span>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transform transition-transform group-hover:rotate-180" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                    </span>
                </button>
            </div>
        {/if}
    {/if}
</div>

<style>
    .line-clamp-2 {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .line-clamp-3 {
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    @keyframes shimmer {
        100% {
            transform: translateX(100%);
        }
    }

    /* Staggered animation for cards */
    a[data-game-id] {
        opacity: 0;
        transform: translateY(20px);
        animation: fadeInUp 0.6s ease forwards;
    }

    @keyframes fadeInUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>