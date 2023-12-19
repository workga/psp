import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Search.css';

export function Search() {
  const [brands, setBrands] = useState([]);
  const [models, setModels] = useState([]);
  const [gens, setGens] = useState([]);
  const [selectedBrandId, setSelectedBrandId] = useState('');
  const [selectedModelId, setSelectedModelId] = useState('');
  const [selectedGenId, setSelectedGenId] = useState('');
  const [brandSearch, setBrandSearch] = useState('');
  const [modelSearch, setModelSearch] = useState('');
  const [genSearch, setGenSearch] = useState('');

  useEffect(() => {
    async function fetchBrands() {
      try {
        const response = await axios.get('/api/cars/brands', {
          params: { search: brandSearch, sort_by: 'score' }
        });
        setBrands(response.data);
      } catch (error) {
        console.error('Error fetching car brands:', error);
      }
    }

    fetchBrands();
  }, [brandSearch]);

  useEffect(() => {
    async function fetchModels() {
      if (selectedBrandId) {
        try {
          const response = await axios.get(`/api/cars/brands/${selectedBrandId}/models`, {
            params: { search: modelSearch, sort_by: 'score' }
          });
          setModels(response.data);
        } catch (error) {
          console.error('Error fetching car models:', error);
        }
      }
    }

    fetchModels();
  }, [selectedBrandId, modelSearch]);

  useEffect(() => {
    async function fetchGens() {
      if (selectedModelId && selectedBrandId) {
        try {
          const response = await axios.get(`/api/cars/brands/${selectedBrandId}/models/${selectedModelId}/gens`, {
            params: { search: genSearch, sort_by: 'score' }
          });
          setGens(response.data);
        } catch (error) {
          console.error('Error fetching car generations:', error);
        }
      }
    }

    fetchGens();
  }, [selectedModelId, selectedBrandId, genSearch]);

  const handleBrandInputChange = (e) => {
    setBrandSearch(e.target.value);
    setModelSearch('');
    setGenSearch('');

    const selectedBrand = brands.find((brand) => brand.brand_name.toLowerCase() === e.target.value.toLowerCase());
    setSelectedBrandId(selectedBrand ? selectedBrand.id : '');
  };

  const handleModelInputChange = (e) => {
    setModelSearch(e.target.value);
    setGenSearch('');

    const selectedModel = models.find((model) => model.model_name.toLowerCase() === e.target.value.toLowerCase());
    setSelectedModelId(selectedModel ? selectedModel.id : '');
  };

  const handleGenInputChange = (e) => {
    setGenSearch(e.target.value);

    const selectedGen = gens.find((gen) => gen.gen_name.toLowerCase() === e.target.value.toLowerCase());
    setSelectedGenId(selectedGen ? selectedGen.id : '');
  };

  return (
    <div className="search-container">
      <h2>Search page placeholder</h2>
      <form className="search-form">
        <label>
          Марка автомобиля:
          <input
            type="text"
            value={brandSearch}
            onChange={handleBrandInputChange}
            list="brandsList"
          />
          <datalist id="brandsList">
            {brands
              .map((brand) => (
                <option key={brand.id} value={brand.brand_name}>
                  {brand.brand_name}
                </option>
              ))}
          </datalist>
        </label>

        <label>
          Модель автомобиля:
          <input
            type="text"
            value={modelSearch}
            onChange={handleModelInputChange}
            list="modelsList"
          />
          <datalist id="modelsList">
            {models
              .map((model) => (
                <option key={model.id} value={model.model_name}>
                  {model.model_name}
                </option>
              ))}
          </datalist>
        </label>

        <label>
          Поколение автомобиля:
          <input
            type="text"
            value={genSearch}
            onChange={handleGenInputChange}
            list="gensList"
          />
          <datalist id="gensList">
            {gens
              .map((gen) => (
                <option key={gen.id} value={gen.gen_name}>
                  {gen.gen_name}
                </option>
              ))}
          </datalist>
        </label>

        <button type="submit">Искать</button>
      </form>
    </div>
  );
}






