<script>
export default {
    props: {
        title: String,
        class: String,
        clickMethod: Function
    }
}
</script>

<template>
    <button :class="class" @click="clickMethod">
        <img src="/assets/download-icon.svg" class="status-icon" alt="Upload feito com sucesso">
        {{ title }}
    </button>
</template>
