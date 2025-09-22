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

<div>
    <div class="text-center mb-12">
        <h2 class="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Featured Games</h2>
        <p class="text-slate-400 text-lg max-w-2xl mx-auto">Explore our curated collection of developer-themed board games, each designed to challenge your technical skills and strategic thinking.</p>
    </div>
    
    {#if loading}
        <!-- loading animation -->
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
            {#each Array(6) as _, i}
                <div class="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-sm rounded-2xl overflow-hidden shadow-xl border border-slate-700/50">
                    <div class="p-8">
                        <div class="animate-pulse">
                            <div class="h-8 bg-gradient-to-r from-slate-700 to-slate-600 rounded-lg w-3/4 mb-4"></div>
                            <div class="flex gap-2 mb-4">
                                <div class="h-6 bg-gradient-to-r from-blue-800/60 to-blue-700/60 rounded-full w-20"></div>
                                <div class="h-6 bg-gradient-to-r from-purple-800/60 to-purple-700/60 rounded-full w-24"></div>
                            </div>
                            <div class="space-y-3 mb-6">
                                <div class="h-4 bg-slate-700 rounded w-full"></div>
                                <div class="h-4 bg-slate-700 rounded w-5/6"></div>
                                <div class="h-4 bg-slate-700 rounded w-4/6"></div>
                            </div>
                            <div class="flex justify-between items-center">
                                <div class="h-6 bg-blue-700/60 rounded w-1/3"></div>
                                <div class="flex gap-2">
                                    <div class="h-8 w-8 bg-slate-700 rounded-lg"></div>
                                    <div class="h-8 w-8 bg-slate-700 rounded-lg"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else if error}
        <!-- error display -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-red-400">{error}</p>
        </div>
    {:else if games.length === 0}
        <!-- no games found -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-slate-300">No games available at the moment.</p>
        </div>
    {:else}
        <!-- game list -->
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8" data-testid="games-grid">
            {#each games as game (game.id)}
                <a 
                    href={`/game/${game.id}`} 
                    class="group block relative bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-sm rounded-2xl overflow-hidden shadow-xl border border-slate-700/50 hover:border-blue-500/50 hover:shadow-blue-500/20 hover:shadow-2xl transition-all duration-500 hover:scale-105 transform-gpu"
                    data-testid="game-card"
                    data-game-id={game.id}
                    data-game-title={game.title}
                >
                    <!-- Background Pattern -->
                    <div class="absolute inset-0 opacity-5 group-hover:opacity-10 transition-opacity duration-500">
                        <div class="absolute inset-0 bg-gradient-to-br from-blue-600/20 via-purple-600/20 to-teal-600/20"></div>
                        <div class="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-2xl"></div>
                        <div class="absolute bottom-0 left-0 w-24 h-24 bg-purple-500/10 rounded-full blur-xl"></div>
                    </div>

                    <!-- Hover Glow Effect -->
                    <div class="absolute inset-0 bg-gradient-to-r from-blue-600/5 via-purple-600/5 to-teal-600/5 opacity-0 group-hover:opacity-100 transition-all duration-500"></div>
                    
                    <div class="relative p-8">
                        <!-- Status Badge -->
                        <div class="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                            <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse shadow-green-500/50 shadow-lg"></div>
                        </div>

                        <div class="relative z-10">
                            <h3 class="text-2xl font-bold text-slate-100 mb-3 group-hover:text-blue-400 transition-colors duration-300 leading-tight" data-testid="game-title">{game.title}</h3>
                            
                            {#if game.category_name || game.publisher_name}
                                <div class="flex flex-wrap gap-2 mb-4">
                                    {#if game.category_name}
                                        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-blue-900/60 to-blue-800/60 text-blue-300 border border-blue-700/50 backdrop-blur-sm" data-testid="game-category">
                                            <span class="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                                            {game.category_name}
                                        </span>
                                    {/if}
                                    {#if game.publisher_name}
                                        <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-purple-900/60 to-purple-800/60 text-purple-300 border border-purple-700/50 backdrop-blur-sm" data-testid="game-publisher">
                                            <span class="w-2 h-2 bg-purple-400 rounded-full mr-2"></span>
                                            {game.publisher_name}
                                        </span>
                                    {/if}
                                </div>
                            {/if}
                            
                            <p class="text-slate-400 mb-6 text-base leading-relaxed line-clamp-3 group-hover:text-slate-300 transition-colors duration-300" data-testid="game-description">{game.description}</p>
                            
                            <!-- Action Button -->
                            <div class="flex items-center justify-between">
                                <div class="text-base text-blue-400 font-semibold flex items-center group-hover:text-blue-300 transition-colors duration-300">
                                    <span>Explore Game</span>
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2 transform transition-all duration-300 group-hover:translate-x-1 group-hover:scale-110" viewBox="0 0 20 20" fill="currentColor">
                                        <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                                    </svg>
                                </div>
                                
                                <!-- Interactive Elements -->
                                <div class="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                                    <button class="p-2 rounded-lg bg-slate-700/50 hover:bg-slate-600/50 text-slate-400 hover:text-slate-200 transition-colors duration-200">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                                        </svg>
                                    </button>
                                    <button class="p-2 rounded-lg bg-slate-700/50 hover:bg-slate-600/50 text-slate-400 hover:text-slate-200 transition-colors duration-200">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Bottom Border Effect -->
                    <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 via-purple-600 to-teal-600 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>
                </a>
            {/each}
        </div>
    {/if}
</div>