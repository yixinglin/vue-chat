<template>
    <ChatWindow></ChatWindow>
    <!-- <v-md-editor v-model="text" height="400px"></v-md-editor> -->


</template>

<script>
import ChatWindow from '@/components/ChatWindow.vue';

export default {
    data() {
        return {
            text: '##aa',
        };
    },
    name: 'ChatView',
    components: {
        ChatWindow
    }
}

</script>