<template>
  <div>
    <h1>New Post</h1>
    <form id="addPostForm" @submit.prevent="addPost">

      <div class="form-group mb-3">
        <label for="photo" class="form-label">Photo:</label>
        <input type="file" name="photo" class="form-control-file" accept="image/jpeg, image/png">
      </div>

      <div class="form-group mb-3">
        <label for="caption" class="form-label">Caption:</label>
        <textarea name="caption" class="form-control"></textarea>
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

function addPost (){
    let addPostForm = document.getElementById('addPostForm'); 
    let form_data = new FormData(addPostForm);

    fetch("/api/v1/users/<user_id>/posts", {
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
        router.push('/explore/');
    })
    .catch(function (error) {
        console.log(error);
    });
};

</script>