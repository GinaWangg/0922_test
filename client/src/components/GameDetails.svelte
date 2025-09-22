<script lang="ts">
    import { onMount } from "svelte";
    
    interface Game {
        id: number;
        title: string;
        description: string;
        publisher: {
            id: number;
            name: string;
        } | null;
        category: {
            id: number;
            name: string;
        } | null;
        starRating: number | null;
    }

    // Accept either a game object or a gameId
    export let game: Game | undefined = undefined;
    export let gameId = 0;
    
    let loading = true;
    let error: string | null = null;
    let gameData: Game | null = null;
    
    onMount(async () => {
        // If game object is provided directly, use it
        if (game) {
            gameData = game;
            loading = false;
            return;
        }
        
        // Otherwise fetch data using gameId
        if (gameId) {
            try {
                const response = await fetch(`/api/games/${gameId}`);
                if (response.ok) {
                    gameData = await response.json();
                } else {
                    error = `Failed to fetch game: ${response.status} ${response.statusText}`;
                }
            } catch (err) {
                error = `Error: ${err instanceof Error ? err.message : String(err)}`;
            } finally {
                loading = false;
            }
        } else {
            error = "No game ID provided";
            loading = false;
        }
    });

    // Function to render stars based on rating
    function renderStarRating(rating: number | null): string {
        if (rating === null) return "Not yet rated";
        
        const fullStars = Math.floor(rating);
        const halfStar = rating % 1 >= 0.5;
        const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
        
        return '★'.repeat(fullStars) + (halfStar ? '½' : '') + '☆'.repeat(emptyStars);
    }
</script>

<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
    {#if loading}
        <!-- Enhanced loading state -->
        <div class="relative overflow-hidden bg-slate-800/40 backdrop-blur-sm rounded-2xl border border-slate-700/50 shadow-xl">
            <div class="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5"></div>
            <div class="relative p-8">
                <div class="animate-pulse space-y-6">
                    <!-- Shimmer effect -->
                    <div class="absolute inset-0 -translate-x-full animate-[shimmer_2s_infinite] bg-gradient-to-r from-transparent via-white/5 to-transparent"></div>
                    
                    <div class="flex justify-between items-start">
                        <div class="flex-1">
                            <div class="h-10 bg-slate-700/60 rounded-lg w-3/4 mb-4"></div>
                            <div class="flex space-x-2 mb-6">
                                <div class="h-6 bg-slate-700/60 rounded-full w-20"></div>
                                <div class="h-6 bg-slate-700/60 rounded-full w-24"></div>
                            </div>
                        </div>
                        <div class="h-8 bg-slate-700/60 rounded-full w-24"></div>
                    </div>
                    
                    <div class="space-y-3">
                        <div class="h-6 bg-slate-700/60 rounded w-1/4"></div>
                        <div class="h-4 bg-slate-700/60 rounded w-full"></div>
                        <div class="h-4 bg-slate-700/60 rounded w-5/6"></div>
                        <div class="h-4 bg-slate-700/60 rounded w-4/6"></div>
                    </div>
                    
                    <div class="h-12 bg-slate-700/60 rounded-xl w-full mt-8"></div>
                </div>
            </div>
        </div>
    {:else if error}
        <!-- Enhanced error state -->
        <div class="text-center py-16">
            <div class="bg-red-500/10 border border-red-500/20 rounded-2xl p-8 max-w-md mx-auto">
                <div class="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-red-400 mb-2">Game Not Found</h3>
                <p class="text-red-300/80 mb-4">{error}</p>
                <a href="/" class="inline-flex items-center bg-red-600 hover:bg-red-500 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                    </svg>
                    Back to Games
                </a>
            </div>
        </div>
    {:else if gameData}
        <!-- Enhanced game details -->
        <div class="relative overflow-hidden bg-slate-800/40 backdrop-blur-sm rounded-2xl border border-slate-700/50 shadow-2xl" data-testid="game-details">
            <!-- Background gradient -->
            <div class="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/5 to-indigo-500/5"></div>
            
            <!-- Animated background elements -->
            <div class="absolute top-0 right-0 w-40 h-40 bg-blue-500/5 rounded-full blur-3xl"></div>
            <div class="absolute bottom-0 left-0 w-40 h-40 bg-purple-500/5 rounded-full blur-3xl"></div>

            <div class="relative p-8 sm:p-10">
                <!-- Header Section -->
                <div class="flex flex-col lg:flex-row lg:justify-between lg:items-start gap-6 mb-8">
                    <div class="flex-1">
                        <h1 class="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-blue-300 bg-clip-text text-transparent mb-4 leading-tight" data-testid="game-details-title">
                            {gameData.title}
                        </h1>
                        
                        <!-- Tags -->
                        <div class="flex flex-wrap gap-3 mb-6">
                            {#if gameData.category}
                                <span class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-blue-500/20 text-blue-300 border border-blue-500/30" data-testid="game-details-category">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                                    </svg>
                                    {gameData.category.name}
                                </span>
                            {/if}
                            {#if gameData.publisher}
                                <span class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-purple-500/20 text-purple-300 border border-purple-500/30" data-testid="game-details-publisher">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                    </svg>
                                    {gameData.publisher.name}
                                </span>
                            {/if}
                        </div>
                    </div>
                    
                    <!-- Rating -->
                    {#if gameData.starRating !== null}
                        <div class="flex items-center space-x-3 bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border border-yellow-500/30 rounded-xl px-4 py-3">
                            <div class="text-2xl text-yellow-400" data-testid="game-rating">
                                {renderStarRating(gameData.starRating)}
                            </div>
                            <div class="text-right">
                                <div class="text-xl font-bold text-yellow-400">{gameData.starRating.toFixed(1)}</div>
                                <div class="text-xs text-yellow-300/80">Rating</div>
                            </div>
                        </div>
                    {/if}
                </div>

                <!-- Description Section -->
                <div class="mb-8">
                    <h2 class="text-2xl font-bold text-slate-100 mb-4 flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-3 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        About This Game
                    </h2>
                    <div class="bg-slate-800/30 backdrop-blur-sm border border-slate-700/30 rounded-xl p-6">
                        <p class="text-slate-300 text-lg leading-relaxed" data-testid="game-details-description">
                            {gameData.description}
                        </p>
                    </div>
                </div>

                <!-- Funding Progress (Placeholder) -->
                <div class="mb-8">
                    <h3 class="text-xl font-semibold text-slate-100 mb-4 flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                        </svg>
                        Funding Progress
                    </h3>
                    <div class="bg-slate-800/30 backdrop-blur-sm border border-slate-700/30 rounded-xl p-6">
                        <div class="flex justify-between items-center mb-3">
                            <span class="text-slate-300">$12,450 raised</span>
                            <span class="text-slate-400">of $25,000 goal</span>
                        </div>
                        <div class="w-full bg-slate-700/50 rounded-full h-3 mb-4">
                            <div class="bg-gradient-to-r from-green-500 to-blue-500 h-3 rounded-full transition-all duration-1000 ease-out" style="width: 49.8%"></div>
                        </div>
                        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
                            <div>
                                <div class="text-2xl font-bold text-green-400">156</div>
                                <div class="text-sm text-slate-400">Backers</div>
                            </div>
                            <div>
                                <div class="text-2xl font-bold text-blue-400">18</div>
                                <div class="text-sm text-slate-400">Days Left</div>
                            </div>
                            <div>
                                <div class="text-2xl font-bold text-purple-400">50%</div>
                                <div class="text-sm text-slate-400">Funded</div>
                            </div>
                            <div>
                                <div class="text-2xl font-bold text-orange-400">$80</div>
                                <div class="text-sm text-slate-400">Avg Pledge</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="flex flex-col sm:flex-row gap-4">
                    <button 
                        class="flex-1 group relative overflow-hidden bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-bold py-4 px-8 rounded-xl shadow-lg hover:shadow-blue-500/25 transition-all duration-300 transform hover:scale-[1.02]" 
                        data-testid="back-game-button"
                    >
                        <div class="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-400 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
                        <span class="relative flex items-center justify-center space-x-3">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                            </svg>
                            <span>Support This Game</span>
                        </span>
                    </button>
                    
                    <button class="group bg-slate-800/60 hover:bg-slate-800/80 backdrop-blur-sm border border-slate-700/50 hover:border-slate-600/50 text-slate-300 hover:text-white font-medium py-4 px-8 rounded-xl transition-all duration-300 transform hover:scale-[1.02]">
                        <span class="flex items-center justify-center space-x-2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                            </svg>
                            <span>Share</span>
                        </span>
                    </button>
                </div>
            </div>
        </div>
    {:else}
        <!-- No game data -->
        <div class="text-center py-16">
            <div class="bg-slate-800/40 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8 max-w-md mx-auto">
                <div class="w-16 h-16 bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                    </svg>
                </div>
                <h3 class="text-lg font-semibold text-slate-300 mb-2">No Game Information</h3>
                <p class="text-slate-400 text-sm mb-4">Unable to load game details at this time.</p>
                <a href="/" class="inline-flex items-center bg-blue-600 hover:bg-blue-500 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200">
                    Back to Games
                </a>
            </div>
        </div>
    {/if}
</div>

<style>
    @keyframes shimmer {
        100% {
            transform: translateX(100%);
        }
    }
</style>