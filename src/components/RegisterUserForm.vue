<template>
  <div>
    <h1>User Registration</h1>
    <form id="registerUserForm" @submit.prevent="registerUser">

      <div class="form-group mb-3">
        <label for="username" class="form-label">Username:</label>
        <input type="text" name="username" class="form-control">
      </div>

      <div class="form-group mb-3">
        <label for="password" class="form-label">Password:</label>
        <input type="password" name="password" class="form-control">
      </div>

      <div class="form-group mb-3">
        <label for="first_name" class="form-label">Firstname:</label>
        <input type="text" name="firstname" class="form-control">
      </div>

      <div class="form-group mb-3">
        <label for="last_name" class="form-label">Lastname:</label>
        <input type="text" name="lastname" class="form-control">
      </div>

      <div class="form-group mb-3">
        <label for="email" class="form-label">Email:</label>
        <input type="text" name="email" class="form-control">
      </div>

      <div class="form-group mb-3">
        <label for="location" class="form-label">Location:</label>
        <input type="text" name="location" class="form-control">
      </div>

      <div class="form-group mb-3">
        <label for="biography" class="form-label">Biography:</label>
        <textarea name="biography" class="form-control"></textarea>
      </div>

      <div class="form-group mb-3">
        <label for="profile_photo" class="form-label">Photo:</label>
        <input type="file" name="photo" class="form-control-file" accept="image/jpeg, image/png">
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

function registerUser (){
    let registerUserForm = document.getElementById('registerUserForm'); 
    let form_data = new FormData(registerUserForm);

    fetch('/api/v1/register', {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value 
        }
    })
    .then(function (response) { 
        console.log(response);
        return response.json(); 
    })
    .then(function (data) {
        console.log(data);
        router.push('/login/');
    })
    .catch(function (error) {
        console.log(error);
    });
};

function getCsrfToken() { 
    fetch('/api/v1/csrf-token') 
    .then((response) => response.json()) 
    .then((data) => { 
        console.log(data); 
        csrf_token.value = data.csrf_token; 
    }) 
}   

</script>