import React, { useState, useMemo } from 'react';
import { Search, Shield, Brain, Zap, Heart, Swords } from 'lucide-react';

// Base de données des Pokémon avec leurs stats
const pokemonData = [
  {
    id: 1,
    name: "Bulbizarre",
    types: ["Plante", "Poison"],
    stats: {
      hp: 45,
      attack: 49,
      defense: 49,
      spAttack: 65,
      spDefense: 65,
      speed: 45
    },
    evYield: { spAttack: 1 },
    sprite: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"
  },
  {
    id: 2,
    name: "Herbizarre",
    types: ["Plante", "Poison"],
    stats: {
      hp: 60,
      attack: 62,
      defense: 63,
      spAttack: 80,
      spDefense: 80,
      speed: 60
    },
    evYield: { spAttack: 1, spDefense: 1 },
    sprite: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png"
  },
  {
    id: 3,
    name: "Florizarre",
    types: ["Plante", "Poison"],
    stats: {
      hp: 80,
      attack: 82,
      defense: 83,
      spAttack: 100,
      spDefense: 100,
      speed: 80
    },
    evYield: { spAttack: 2, spDefense: 1 },
    sprite: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/3.png"
  },
  {
    id: 4,
    name: "Salamèche",
    types: ["Feu"],
    stats: {
      hp: 39,
      attack: 52,
      defense: 43,
      spAttack: 60,
      spDefense: 50,
      speed: 65
    },
    evYield: { speed: 1 },
    sprite: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png"
  },
  {
    id: 5,
    name: "Reptincel",
    types: ["Feu"],
    stats: {
      hp: 58,
      attack: 64,
      defense: 58,
      spAttack: 80,
      spDefense: 65,
      speed: 80
    },
    evYield: { speed: 1, spAttack: 1 },
    sprite: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/5.png"
  },
  {
    id: 6,
    name: "Dracaufeu",
    types: ["Feu", "Vol"],
    stats: {
      hp: 78,
      attack: 84,
      defense: 78,
      spAttack: 109,
      spDefense: 85,
      speed: 100
    },
    evYield: { spAttack: 3 },
    sprite: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png"
  },
  {
    id: 7,
    name: "Carapuce",
    types: ["Eau"],
    stats: {
      hp: 44,
      attack: 48,
      defense: 65,
      spAttack: 50,
      spDefense: 64,
      speed: 43
    },
    evYield: { defense: 1 },
    sprite: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png"
  },
  {
    id: 8,
    name: "Carabaffe",
    types: ["Eau"],
    stats: {
      hp: 59,
      attack: 63,
      defense: 80,
      spAttack: 65,
      spDefense: 80,
      speed: 58
    },
    evYield: { defense: 1, spDefense: 1 },
    sprite: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/8.png"
  },
  {
    id: 9,
    name: "Tortank",
    types: ["Eau"],
    stats: {
      hp: 79,
      attack: 83,
      defense: 100,
      spAttack: 85,
      spDefense: 105,
      speed: 78
    },
    evYield: { spDefense: 3 },
    sprite: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png"
  },
  {
    id: 25,
    name: "Pikachu",
    types: ["Électrik"],
    stats: {
      hp: 35,
      attack: 55,
      defense: 40,
      spAttack: 50,
      spDefense: 50,
      speed: 90
    },
    evYield: { speed: 2 },
    sprite: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
  }
];

// Couleurs des types
const typeColors = {
  "Normal": "#A8A878",
  "Feu": "#F08030",
  "Eau": "#6890F0",
  "Électrik": "#F8D030",
  "Plante": "#78C850",
  "Glace": "#98D8D8",
  "Combat": "#C03028",
  "Poison": "#A040A0",
  "Sol": "#E0C068",
  "Vol": "#A890F0",
  "Psy": "#F85888",
  "Insecte": "#A8B820",
  "Roche": "#B8A038",
  "Spectre": "#705898",
  "Dragon": "#7038F8",
  "Ténèbres": "#705848",
  "Acier": "#B8B8D0",
  "Fée": "#EE99AC"
};

// Icônes pour les stats
const statIcons = {
  hp: Heart,
  attack: Swords,
  defense: Shield,
  spAttack: Zap,
  spDefense: Brain,
  speed: Zap
};

const statNames = {
  hp: "PV",
  attack: "Attaque",
  defense: "Défense",
  spAttack: "Attaque Spé.",
  spDefense: "Défense Spé.",
  speed: "Vitesse"
};

export default function Pokedex() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedPokemon, setSelectedPokemon] = useState(null);
  const [filterType, setFilterType] = useState("Tous");

  // Obtenir tous les types uniques
  const allTypes = useMemo(() => {
    const types = new Set(["Tous"]);
    pokemonData.forEach(pokemon => {
      pokemon.types.forEach(type => types.add(type));
    });
    return Array.from(types);
  }, []);

  // Filtrer les Pokémon
  const filteredPokemon = useMemo(() => {
    return pokemonData.filter(pokemon => {
      const matchesSearch = pokemon.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          pokemon.id.toString().includes(searchTerm);
      const matchesType = filterType === "Tous" || pokemon.types.includes(filterType);
      return matchesSearch && matchesType;
    });
  }, [searchTerm, filterType]);

  // Formater les EVs
  const formatEVs = (evYield) => {
    return Object.entries(evYield)
      .map(([stat, value]) => `${value} ${statNames[stat]}`)
      .join(", ");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-gray-800 mb-8">
          Pokédex Interactif
        </h1>

        {/* Barre de recherche et filtres */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-3 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Rechercher un Pokémon..."
                className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <select
              className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
            >
              {allTypes.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Liste des Pokémon */}
          <div className="lg:col-span-2">
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
              {filteredPokemon.map(pokemon => (
                <div
                  key={pokemon.id}
                  onClick={() => setSelectedPokemon(pokemon)}
                  className="bg-white rounded-lg shadow-md p-4 cursor-pointer transform transition-all hover:scale-105 hover:shadow-lg"
                >
                  <img
                    src={pokemon.sprite}
                    alt={pokemon.name}
                    className="w-24 h-24 mx-auto"
                  />
                  <p className="text-center text-gray-600 text-sm">#{pokemon.id.toString().padStart(3, '0')}</p>
                  <h3 className="text-center font-semibold">{pokemon.name}</h3>
                  <div className="flex justify-center gap-1 mt-2">
                    {pokemon.types.map(type => (
                      <span
                        key={type}
                        className="px-2 py-1 text-xs text-white rounded"
                        style={{ backgroundColor: typeColors[type] }}
                      >
                        {type}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Détails du Pokémon sélectionné */}
          <div className="lg:col-span-1">
            {selectedPokemon ? (
              <div className="bg-white rounded-lg shadow-lg p-6 sticky top-4">
                <img
                  src={selectedPokemon.sprite}
                  alt={selectedPokemon.name}
                  className="w-32 h-32 mx-auto mb-4"
                />
                <h2 className="text-2xl font-bold text-center mb-2">
                  {selectedPokemon.name}
                </h2>
                <p className="text-center text-gray-600 mb-4">
                  #{selectedPokemon.id.toString().padStart(3, '0')}
                </p>

                {/* Types */}
                <div className="flex justify-center gap-2 mb-6">
                  {selectedPokemon.types.map(type => (
                    <span
                      key={type}
                      className="px-3 py-1 text-sm text-white rounded-full"
                      style={{ backgroundColor: typeColors[type] }}
                    >
                      {type}
                    </span>
                  ))}
                </div>

                {/* EVs */}
                <div className="bg-purple-50 rounded-lg p-4 mb-6">
                  <h3 className="font-semibold text-purple-800 mb-2">EVs donnés</h3>
                  <p className="text-purple-700">{formatEVs(selectedPokemon.evYield)}</p>
                </div>

                {/* Stats principales */}
                <div className="bg-blue-50 rounded-lg p-4 mb-6">
                  <h3 className="font-semibold text-blue-800 mb-3">Stats défensives</h3>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Shield className="text-blue-600" size={18} />
                        <span className="text-sm">Défense</span>
                      </div>
                      <span className="font-bold text-blue-700">{selectedPokemon.stats.defense}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Brain className="text-purple-600" size={18} />
                        <span className="text-sm">Défense Spé.</span>
                      </div>
                      <span className="font-bold text-purple-700">{selectedPokemon.stats.spDefense}</span>
                    </div>
                  </div>
                </div>

                {/* Toutes les stats */}
                <div>
                  <h3 className="font-semibold mb-3">Toutes les stats</h3>
                  <div className="space-y-3">
                    {Object.entries(selectedPokemon.stats).map(([stat, value]) => {
                      const Icon = statIcons[stat];
                      const maxStat = 255;
                      const percentage = (value / maxStat) * 100;
                      
                      return (
                        <div key={stat}>
                          <div className="flex items-center justify-between mb-1">
                            <div className="flex items-center gap-2">
                              <Icon size={16} className="text-gray-600" />
                              <span className="text-sm">{statNames[stat]}</span>
                            </div>
                            <span className="text-sm font-semibold">{value}</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-gradient-to-r from-blue-400 to-blue-600 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${percentage}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-lg p-6 text-center text-gray-500">
                <p>Sélectionnez un Pokémon pour voir ses détails</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}