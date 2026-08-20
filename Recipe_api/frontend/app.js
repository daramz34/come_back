const API_BASE = window.RECIPE_API_BASE || "/api/v1";
const state = {
  token: localStorage.getItem("recipe_token"),
  user: JSON.parse(localStorage.getItem("recipe_user") || "null"),
  authMode: "login"
};
const $ = (selector) => document.querySelector(selector);

async function request(path, options = {}) {
  const headers = { ...(options.body ? { "Content-Type": "application/json" } : {}), ...(options.headers || {}) };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || data.message || "Something went wrong. Please try again.");
  return data;
}

function setStatus(target, message, error = false) {
  if (!target) return;
  target.textContent = message;
  target.classList.toggle("error", error);
}

function updateHeader() {
  const userLabel = $("#user-label");
  const authButton = $("#auth-button");
  const logoutButton = $("#logout-button");
  if (userLabel) userLabel.textContent = state.user ? `Hi, ${state.user.username}` : "";
  if (authButton) authButton.classList.toggle("hidden", Boolean(state.user));
  if (logoutButton) logoutButton.classList.toggle("hidden", !state.user);
}

async function updateSavedCount() {
  const count = $("#saved-count");
  if (!count || !state.token) {
    if (count && !state.token) count.textContent = "0";
    return;
  }
  try {
    const result = await request("/recipes/favourites");
    const recipes = Array.isArray(result) ? result : result.results || [];
    count.textContent = recipes.length;
  } catch {
    count.textContent = "0";
  }
}

function logout() {
  localStorage.removeItem("recipe_token");
  localStorage.removeItem("recipe_user");
  state.token = null;
  state.user = null;
  window.location.href = "index.html";
}

function setupNavigation() {
  $("#logout-button")?.addEventListener("click", logout);
  $("#menu-button")?.addEventListener("click", () => $(".main-nav")?.classList.toggle("open"));
}

function saveRecipeForNextPage(recipe) {
  sessionStorage.setItem("selected_recipe", JSON.stringify(recipe));
  window.location.href = `recipe.html${recipe.id ? `?id=${encodeURIComponent(recipe.id)}` : ""}`;
}

async function initialiseDiscover() {
  const form = $("#suggestion-form");
  if (!form) return;
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const status = $("#suggestion-status");
    if (!state.token) {
      setStatus(status, "Please sign in before asking for suggestions.", true);
      window.location.href = "auth.html?return=discover";
      return;
    }
    setStatus(status, "Finding delicious possibilities...");
    try {
      const payload = Object.fromEntries(new FormData(form).entries());
      const result = await request("/recipes/suggest", { method: "POST", body: JSON.stringify(payload) });
      const suggestions = Array.isArray(result.suggestions) ? result.suggestions : [];
      renderSuggestions(suggestions, result.id);
      setStatus(status, "Choose a meal to create its full recipe.");
    } catch (error) {
      setStatus(status, error.message, true);
    }
  });
}

function renderSuggestions(items, suggestionId) {
  const container = $("#suggestions");
  container.innerHTML = items.map((item, index) => {
    const name = typeof item === "string" ? item : item.meal_name || item.name;
    const id = typeof item === "object" ? item.id || suggestionId : suggestionId;
    return `<article class="suggestion-card"><span class="card-number">0${index + 1}</span><h3>${escapeHtml(name)}</h3><button type="button" data-meal="${escapeAttr(name)}" data-suggestion="${id}">Create this recipe →</button></article>`;
  }).join("");
  container.querySelectorAll("[data-meal]").forEach((button) => button.addEventListener("click", () => generateRecipe(button.dataset.meal, button.dataset.suggestion)));
}

async function generateRecipe(mealName, suggestionId) {
  const status = $("#suggestion-status");
  setStatus(status, "Writing your recipe...");
  try {
    const recipe = await request("/recipes/generate", {
      method: "POST",
      body: JSON.stringify({ meal_name: mealName, suggestion_id: Number(suggestionId) })
    });
    saveRecipeForNextPage(recipe);
  } catch (error) {
    setStatus(status, error.message, true);
  }
}

async function initialiseAuth() {
  const form = $("#auth-form");
  if (!form) return;
  document.querySelectorAll(".auth-tabs button").forEach((tab) => tab.addEventListener("click", () => {
    state.authMode = tab.dataset.mode;
    document.querySelectorAll(".auth-tabs button").forEach((item) => item.classList.toggle("active", item === tab));
    document.querySelectorAll(".register-only").forEach((field) => field.classList.toggle("hidden", state.authMode !== "register"));
    $(".login-only")?.classList.toggle("hidden", state.authMode === "register");
    $(".submit-button").innerHTML = state.authMode === "register" ? "Create account <span>→</span>" : "Sign in <span>→</span>";
    $("#auth-title").textContent = state.authMode === "register" ? "Start your recipe collection." : "Make yourself at home.";
  }));
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const status = $("#auth-status");
    try {
      let username = formData.get("login_username");
      if (state.authMode === "register") {
        username = formData.get("username");
        await request("/auth/register", {
          method: "POST",
          body: JSON.stringify({ username, email: formData.get("email"), password: formData.get("password") })
        });
      }
      const login = await request("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ username, password: formData.get("password") })
      });
      state.token = login.access_token;
      state.user = { username };
      localStorage.setItem("recipe_token", state.token);
      localStorage.setItem("recipe_user", JSON.stringify(state.user));
      window.location.href = new URLSearchParams(window.location.search).get("return") === "discover" ? "index.html#planner" : "collections.html";
    } catch (error) {
      setStatus(status, error.message, true);
    }
  });
}

function renderRecipe(recipe) {
  $("#recipe-detail").innerHTML = `<p class="eyebrow">Your recipe</p><h1>${escapeHtml(recipe.meal_name)}</h1><div class="recipe-meta">${escapeHtml([recipe.cuisine_type, recipe.dietary_preference, recipe.cooking_time].filter(Boolean).join(" · "))}</div><div class="recipe-columns"><div><h2>Ingredients</h2><p>${escapeHtml(recipe.ingredients || "No ingredients provided.")}</p></div><div><h2>Process</h2><p>${escapeHtml(recipe.steps || "No process provided.")}</p></div></div>${recipe.tips ? `<p class="tips"><strong>Tip:</strong> ${escapeHtml(recipe.tips)}</p>` : ""}<div class="detail-actions"><button id="save-recipe-button" class="button button-coral" type="button">${recipe.is_favourite ? "Saved ✓" : "Save recipe ♡"}</button><a class="button button-ghost" href="index.html">Discover another →</a></div><div id="recipe-status" class="status"></div>`;
  $("#save-recipe-button").addEventListener("click", async () => {
    try {
      await request(`/recipes/${recipe.id}`, { method: "PATCH", body: JSON.stringify({ is_favourite: !recipe.is_favourite }) });
      recipe.is_favourite = !recipe.is_favourite;
      $("#save-recipe-button").textContent = recipe.is_favourite ? "Saved ✓" : "Save recipe ♡";
    } catch (error) { setStatus($("#recipe-status"), error.message, true); }
  });
}

async function initialiseRecipe() {
  if (!$("#recipe-detail")) return;
  if (!state.token) { window.location.href = "auth.html"; return; }
  try {
    const id = new URLSearchParams(window.location.search).get("id");
    const stored = JSON.parse(sessionStorage.getItem("selected_recipe") || "null");
    const recipe = id ? await request(`/recipes/${id}`) : stored;
    if (!recipe) throw new Error("Recipe could not be found.");
    renderRecipe(recipe);
  } catch (error) { setStatus($("#recipe-detail"), error.message, true); }
}

async function initialiseCollections() {
  const grid = $("#collection-grid");
  if (!grid) return;
  if (!state.token) { grid.innerHTML = '<p class="empty-state">Sign in to view your collection.</p>'; return; }
  try {
    const result = await request("/recipes/favourites");
    const recipes = result.results || result;
    grid.innerHTML = recipes.length ? recipes.map((recipe) => `<a class="recipe-card" href="recipe.html?id=${recipe.id}"><p class="eyebrow">Saved recipe</p><h2>${escapeHtml(recipe.meal_name)}</h2><div class="recipe-meta">${escapeHtml([recipe.cuisine_type, recipe.cooking_time].filter(Boolean).join(" · "))}</div><span class="card-link">Read recipe →</span></a>`).join("") : '<p class="empty-state">Nothing saved yet. Discover your next favourite meal.</p>';
  } catch (error) { setStatus(grid, error.message, true); }
}

function escapeHtml(value) { return String(value || "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[char])); }
function escapeAttr(value) { return escapeHtml(value); }

updateHeader();
updateSavedCount();
setupNavigation();
initialiseDiscover();
initialiseAuth();
initialiseRecipe();
initialiseCollections();
