<template>
  <div>
    <h1>User Login</h1>
    <form id="loginForm" @submit.prevent="loginUser">

      <div class="form-group mb-3">
        <label for="username" class="form-label">Username:</label>
        <input type="text" name="username" class="form-control">
      </div>

      <div class="form-group mb-3">
      <label for="password" class="form-label">Password:</label>
      <input type="password" name="password" class="form-control">
      </div>

      <button type="submit" class="btn btn-primary">Submit</button>

    </form>
  </div>
</template>

<script setup>

import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
let csrf_token = ref("");

const router = useRouter();

onMounted(() => { 
    getCsrfToken(); 
}); 

function getCsrfToken() { 
    fetch('/api/v1/csrf-token') 
    .then((response) => response.json()) 
    .then((data) => { 
        console.log(data); 
        csrf_token.value = data.csrf_token; 
    }) 
} 

function loginUser (){
    let loginForm = document.getElementById('loginForm'); 
    let form_data = new FormData(loginForm);

    fetch("/api/v1/auth/login", {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value 
        }
    })
    .then(function (response) { 
        return response.json(); 
    })
    .then(function (data) {
        console.log(data);
        if (data.message === "Login Successful"){
            router.push('/explore/');
        } else {
            console.error(data.message);
        }
    })
    .catch(function (error) {
        console.log(error);
    });
};

</script>