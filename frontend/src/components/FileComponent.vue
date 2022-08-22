<script>
export default {
    props: {
        filename: String,
        accept: String,
        class: String,
        name: String,
        id: String,
        disabled: Boolean,
        changeMethod: Function
    }
}
</script>

<template>
    <label :for="id" :class="class">
        <img src="/assets/upload-icon.svg" class="board-inventory-icon" alt="Welcome to PadUtil">      
        {{ filename }}
    </label>
    <input 
        type="file" 
        :name="name" 
        :id="id" 
        :accept="accept"
        @change="changeMethod"
        :disabled="disabled"
    >
</template>