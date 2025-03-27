// app/static/js/meals.js
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar data atual
    const today = new Date();
    const dateSelector = document.getElementById('date-selector');
    dateSelector.value = today.toISOString().split('T')[0];
    
    // Carregar refeições para a data atual
    loadMeals(dateSelector.value);
    
    // Event listeners para navegação de datas
    document.getElementById('prev-day').addEventListener('click', function() {
        const currentDate = new Date(dateSelector.value);
        currentDate.setDate(currentDate.getDate() - 1);
        dateSelector.value = currentDate.toISOString().split('T')[0];
        loadMeals(dateSelector.value);
    });
    
    document.getElementById('next-day').addEventListener('click', function() {
        const currentDate = new Date(dateSelector.value);
        currentDate.setDate(currentDate.getDate() + 1);
        dateSelector.value = currentDate.toISOString().split('T')[0];
        loadMeals(dateSelector.value);
    });
    
    document.getElementById('today-btn').addEventListener('click', function() {
        dateSelector.value = new Date().toISOString().split('T')[0];
        loadMeals(dateSelector.value);
    });
    
    dateSelector.addEventListener('change', function() {
        loadMeals(this.value);
    });
    
    // Inicializar modal de nova refeição
    document.getElementById('mealModal').addEventListener('show.bs.modal', function() {
        // Definir data atual
        document.getElementById('meal-date').value = dateSelector.value;
        
        // Definir hora atual
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        document.getElementById('meal-time').value = `${hours}:${minutes}`;
    });
    
    // Event listener para pesquisa de alimentos
    document.getElementById('search-food-btn').addEventListener('click', searchFoods);
    document.getElementById('food-search').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchFoods();
        }
    });
    
    // Event listener para botão de salvar refeição
    document.getElementById('save-meal').addEventListener('click', saveMeal);
    
    // Event listener para botão de salvar novo alimento
    document.getElementById('save-food').addEventListener('click', saveFood);
});

// Carregar refeições para uma data específica
function loadMeals(date) {
    // Carregar resumo nutricional
    loadNutritionSummary(date);
    
    // Buscar refeições
    axios.get('/api/meals', { params: { date } })
        .then(response => {
            if (response.data.status === 'success') {
                const meals = response.data.meals;
                renderMeals(meals);
            }
        })
        .catch(error => {
            console.error('Erro ao carregar refeições:', error);
        });
}

// Carregar resumo nutricional
function loadNutritionSummary(date) {
    axios.get('/api/meals/nutrition-summary', { params: { date } })
        .then(response => {
            if (response.data.status === 'success') {
                const summary = response.data.summary;
                
                // Atualizar contadores
                document.getElementById('total-calories').textContent = Math.round(summary.total_calories);
                document.getElementById('total-protein').textContent = `${Math.round(summary.total_protein)}g`;
                document.getElementById('total-carbs').textContent = `${Math.round(summary.total_carbs)}g`;
                document.getElementById('total-fat').textContent = `${Math.round(summary.total_fat)}g`;
                
                // Calcular porcentagens para a barra de progresso
                const totalMacros = summary.total_protein + summary.total_carbs + summary.total_fat;
                
                if (totalMacros > 0) {
                    const proteinPercentage = (summary.total_protein / totalMacros) * 100;
                    const carbsPercentage = (summary.total_carbs / totalMacros) * 100;
                    const fatPercentage = (summary.total_fat / totalMacros) * 100;
                    
                    // Atualizar barras de progresso
                    const proteinBar = document.getElementById('protein-bar');
                    const carbsBar = document.getElementById('carbs-bar');
                    const fatBar = document.getElementById('fat-bar');
                    
                    proteinBar.style.width = `${proteinPercentage}%`;
                    proteinBar.textContent = `${Math.round(proteinPercentage)}%`;
                    proteinBar.setAttribute('aria-valuenow', proteinPercentage);
                    
                    carbsBar.style.width = `${carbsPercentage}%`;
                    carbsBar.textContent = `${Math.round(carbsPercentage)}%`;
                    carbsBar.setAttribute('aria-valuenow', carbsPercentage);
                    
                    fatBar.style.width = `${fatPercentage}%`;
                    fatBar.textContent = `${Math.round(fatPercentage)}%`;
                    fatBar.setAttribute('aria-valuenow', fatPercentage);
                } else {
                    // Reset barras de progresso
                    const proteinBar = document.getElementById('protein-bar');
                    const carbsBar = document.getElementById('carbs-bar');
                    const fatBar = document.getElementById('fat-bar');
                    
                    proteinBar.style.width = '0%';
                    proteinBar.textContent = '0%';
                    proteinBar.setAttribute('aria-valuenow', 0);
                    
                    carbsBar.style.width = '0%';
                    carbsBar.textContent = '0%';
                    carbsBar.setAttribute('aria-valuenow', 0);
                    
                    fatBar.style.width = '0%';
                    fatBar.textContent = '0%';
                    fatBar.setAttribute('aria-valuenow', 0);
                }
            }
        })
        .catch(error => {
            console.error('Erro ao carregar resumo nutricional:', error);
        });
}

// Renderizar refeições
function renderMeals(meals) {
    const container = document.getElementById('meals-container');
    
    if (meals.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center">
                <p>Nenhuma refeição registrada para esta data.</p>
                <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#mealModal">
                    <i class="bi bi-plus-circle"></i> Adicionar Refeição
                </button>
            </div>
        `;
        return;
    }
    
    // Ordenar refeições por tipo
    const mealOrder = {
        'breakfast': 1,
        'snack': 2,
        'lunch': 3,
        'dinner': 4
    };
    
    meals.sort((a, b) => {
        return mealOrder[a.meal_type] - mealOrder[b.meal_type];
    });
    
    let html = '';
    
    meals.forEach(meal => {
        // Definir título e ícone com base no tipo de refeição
        let title = '';
        let icon = '';
        
        switch (meal.meal_type) {
            case 'breakfast':
                title = 'Café da Manhã';
                icon = 'bi-cup-hot';
                break;
            case 'lunch':
                title = 'Almoço';
                icon = 'bi-egg-fried';
                break;
            case 'dinner':
                title = 'Jantar';
                icon = 'bi-moon-stars';
                break;
            case 'snack':
                title = 'Lanche';
                icon = 'bi-apple';
                break;
        }
        
        html += `
            <div class="col-lg-6 mb-4">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="card-title mb-0">
                            <i class="bi ${icon} me-2"></i> ${title}
                        </h5>
                        <small class="text-muted">${formatDate(meal.time, false)}</small>
                    </div>
                    <div class="card-body">
        `;
        
        if (meal.notes) {
            html += `<p class="card-text mb-3">${meal.notes}</p>`;
        }
        
        if (meal.items.length === 0) {
            html += `<p class="text-center">Nenhum alimento registrado</p>`;
        } else {
            html += `
                <div class="table-responsive">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Alimento</th>
                                <th>Qtd</th>
                                <th>Calorias</th>
                                <th>Proteínas</th>
                                <th>Carboidratos</th>
                                <th>Gorduras</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            meal.items.forEach(item => {
                html += `
                    <tr>
                        <td>${item.food_name}</td>
                        <td>${item.quantity} ${item.unit}</td>
                        <td>${Math.round(item.calories)}</td>
                        <td>${Math.round(item.protein)}g</td>
                        <td>${Math.round(item.carbs)}g</td>
                        <td>${Math.round(item.fat)}g</td>
                    </tr>
                `;
            });
            
            html += `
                        </tbody>
                        <tfoot>
                            <tr class="table-light">
                                <th colspan="2">Total</th>
                                <th>${Math.round(meal.total_calories)}</th>
                                <th>${Math.round(meal.total_protein)}g</th>
                                <th>${Math.round(meal.total_carbs)}g</th>
                                <th>${Math.round(meal.total_fat)}g</th>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            `;
        }
        
        html += `
                    </div>
                    <div class="card-footer d-flex justify-content-end">
                        <button class="btn btn-sm btn-primary me-2 edit-meal-btn" data-id="${meal.id}">
                            <i class="bi bi-pencil"></i> Editar
                        </button>
                        <button class="btn btn-sm btn-danger delete-meal-btn" data-id="${meal.id}">
                            <i class="bi bi-trash"></i> Excluir
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
    
    // Adicionar event listeners
    document.querySelectorAll('.edit-meal-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const mealId = this.dataset.id;
            editMeal(mealId);
        });
    });
    
    document.querySelectorAll('.delete-meal-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const mealId = this.dataset.id;
            if (confirm('Tem certeza que deseja excluir esta refeição?')) {
                deleteMeal(mealId);
            }
        });
    });
}

// Pesquisar alimentos
function searchFoods() {
    const query = document.getElementById('food-search').value.trim();
    
    if (!query) return;
    
    axios.get('/api/meals/food-items', { params: { query } })
        .then(response => {
            if (response.data.status === 'success') {
                const foods = response.data.food_items;
                const resultsContainer = document.getElementById('search-results');
                const resultsList = document.getElementById('food-results');
                
                if (foods.length === 0) {
                    resultsList.innerHTML = `
                        <div class="list-group-item">
                            <p class="mb-0">Nenhum alimento encontrado</p>
                        </div>
                    `;
                } else {
                    let html = '';
                    
                    foods.forEach(food => {
                        html += `
                            <button type="button" class="list-group-item list-group-item-action food-item-btn" 
                                data-id="${food.id}" 
                                data-name="${food.name}" 
                                data-calories="${food.calories}" 
                                data-protein="${food.protein}" 
                                data-carbs="${food.carbs}" 
                                data-fat="${food.fat}">
                                <div class="d-flex justify-content-between align-items-center">
                                    <strong>${food.name}</strong>
                                    <span class="badge bg-primary">${Math.round(food.calories)} cal</span>
                                </div>
                                <small class="text-muted">
                                    Proteínas: ${food.protein}g | Carboidratos: ${food.carbs}g | Gorduras: ${food.fat}g
                                </small>
                            </button>
                        `;
                    });
                    
                    resultsList.innerHTML = html;
                    
                    // Adicionar event listeners para os botões de alimentos
                    document.querySelectorAll('.food-item-btn').forEach(btn => {
                        btn.addEventListener('click', function() {
                            addFoodToMeal(this.dataset);
                        });
                    });
                }
                
                resultsContainer.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Erro ao pesquisar alimentos:', error);
        });
}

// Adicionar alimento à refeição
let temporaryMealItems = [];

function addFoodToMeal(foodData) {
    const foodId = foodData.id;
    const foodName = foodData.name;
    const calories = parseFloat(foodData.calories);
    const protein = parseFloat(foodData.protein);
    const carbs = parseFloat(foodData.carbs);
    const fat = parseFloat(foodData.fat);
    
    // Adicionar item à lista temporária
    const mealItem = {
        food_id: foodId,
        food_name: foodName,
        quantity: 1,
        unit: 'porção',
        calories: calories,
        protein: protein,
        carbs: carbs,
        fat: fat
    };
    
    temporaryMealItems.push(mealItem);
    
    // Atualizar tabela de itens
    updateMealItemsTable();
    
    // Limpar pesquisa
    document.getElementById('food-search').value = '';
    document.getElementById('search-results').style.display = 'none';
}

// Atualizar tabela de itens da refeição
function updateMealItemsTable() {
    const tableBody = document.getElementById('meal-items');
    const noItemsRow = document.getElementById('no-items-row');
    
    if (temporaryMealItems.length === 0) {
        noItemsRow.style.display = 'table-row';
        document.getElementById('meal-total-calories').textContent = '0';
        return;
    }
    
    noItemsRow.style.display = 'none';
    
    let html = '';
    let totalCalories = 0;
    
    temporaryMealItems.forEach((item, index) => {
        const itemCalories = item.calories * item.quantity;
        totalCalories += itemCalories;
        
        html += `
            <tr>
                <td>${item.food_name}</td>
                <td>
                    <input type="number" class="form-control form-control-sm quantity-input" 
                        data-index="${index}" value="${item.quantity}" min="0.1" step="0.1" style="width: 80px">
                </td>
                <td>
                    <select class="form-select form-select-sm unit-select" data-index="${index}" style="width: 100px">
                        <option value="porção" ${item.unit === 'porção' ? 'selected' : ''}>porção</option>
                        <option value="g" ${item.unit === 'g' ? 'selected' : ''}>g</option>
                        <option value="ml" ${item.unit === 'ml' ? 'selected' : ''}>ml</option>
                        <option value="unidade" ${item.unit === 'unidade' ? 'selected' : ''}>unidade</option>
                    </select>
                </td>
                <td>${Math.round(itemCalories)}</td>
                <td>
                    <button type="button" class="btn btn-sm btn-danger remove-item-btn" data-index="${index}">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = html;
    document.getElementById('meal-total-calories').textContent = Math.round(totalCalories);
    
    // Adicionar event listeners
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', function() {
            const index = parseInt(this.dataset.index);
            const newQuantity = parseFloat(this.value);
            
            if (newQuantity <= 0) {
                this.value = temporaryMealItems[index].quantity;
                return;
            }
            
            temporaryMealItems[index].quantity = newQuantity;
            updateMealItemsTable();
        });
    });
    
    document.querySelectorAll('.unit-select').forEach(select => {
        select.addEventListener('change', function() {
            const index = parseInt(this.dataset.index);
            temporaryMealItems[index].unit = this.value;
        });
    });
    
    document.querySelectorAll('.remove-item-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const index = parseInt(this.dataset.index);
            temporaryMealItems.splice(index, 1);
            updateMealItemsTable();
        });
    });
}

// Salvar refeição
function saveMeal() {
    // Obter dados do formulário
    const mealType = document.getElementById('meal-type').value;
    const mealDate = document.getElementById('meal-date').value;
    const mealTime = document.getElementById('meal-time').value;
    const notes = document.getElementById('meal-notes').value;
    
    // Validar dados
    if (!mealType || !mealDate || !mealTime) {
        alert('Por favor, preencha os campos obrigatórios.');
        return;
    }
    
    // Validar se há itens na refeição
    if (temporaryMealItems.length === 0) {
        alert('Por favor, adicione pelo menos um alimento à refeição.');
        return;
    }
    
    // Preparar dados para envio
    const data = {
        meal_type: mealType,
        date: mealDate,
        time: `${mealDate}T${mealTime}:00`,
        notes: notes,
        items: temporaryMealItems.map(item => ({
            food_id: item.food_id,
            quantity: item.quantity,
            unit: item.unit
        }))
    };
    
    // Enviar requisição
    axios.post('/api/meals', data)
        .then(response => {
            if (response.data.status === 'success') {
                // Limpar formulário
                document.getElementById('meal-form').reset();
                temporaryMealItems = [];
                updateMealItemsTable();
                
                // Fechar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('mealModal'));
                modal.hide();
                
                // Atualizar lista de refeições
                loadMeals(mealDate);
                
                // Exibir mensagem de sucesso
                alert('Refeição registrada com sucesso!');
            }
        })
        .catch(error => {
            console.error('Erro ao salvar refeição:', error);
            alert('Ocorreu um erro ao salvar a refeição. Por favor, tente novamente.');
        });
}

// Editar refeição
function editMeal(mealId) {
    // Funcionalidade a ser implementada
    alert('Edição de refeição será implementada em breve!');
}

// Excluir refeição
function deleteMeal(mealId) {
    axios.delete(`/api/meals/${mealId}`)
        .then(response => {
            if (response.data.status === 'success') {
                // Recarregar lista de refeições
                loadMeals(document.getElementById('date-selector').value);
                
                // Exibir mensagem de sucesso
                alert('Refeição excluída com sucesso!');
            }
        })
        .catch(error => {
            console.error('Erro ao excluir refeição:', error);
            alert('Ocorreu um erro ao excluir a refeição. Por favor, tente novamente.');
        });
}

// Salvar novo alimento
function saveFood() {
    // Obter dados do formulário
    const name = document.getElementById('food-name').value;
    const calories = parseFloat(document.getElementById('food-calories').value);
    const protein = parseFloat(document.getElementById('food-protein').value);
    const carbs = parseFloat(document.getElementById('food-carbs').value);
    const fat = parseFloat(document.getElementById('food-fat').value);
    const fiber = parseFloat(document.getElementById('food-fiber').value || 0);
    
    // Validar dados
    if (!name || isNaN(calories) || isNaN(protein) || isNaN(carbs) || isNaN(fat)) {
        alert('Por favor, preencha os campos obrigatórios.');
        return;
    }
    
    // Preparar dados para envio
    const data = {
        name,
        calories,
        protein,
        carbs,
        fat,
        fiber
    };
    
    // Enviar requisição
    axios.post('/api/meals/food-items', data)
        .then(response => {
            if (response.data.status === 'success') {
                const food = response.data.food_item;
                
                // Adicionar alimento à refeição
                addFoodToMeal({
                    id: food.id,
                    name: food.name,
                    calories: food.calories,
                    protein: food.protein,
                    carbs: food.carbs,
                    fat: food.fat
                });
                
                // Limpar formulário
                document.getElementById('food-form').reset();
                
                // Fechar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('newFoodModal'));
                modal.hide();
                
                // Exibir mensagem de sucesso
                alert('Alimento criado com sucesso!');
            }
        })
        .catch(error => {
            console.error('Erro ao salvar alimento:', error);
            alert('Ocorreu um erro ao salvar o alimento. Por favor, tente novamente.');
        });
}