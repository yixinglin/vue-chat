<template>
    <div class="wechat-web">
      <div class="sidebar">
        <el-menu :default-active="activeChat" class="sidebar-menu" @select="selectChat">
          <el-menu-item v-for="(chat, index) in chats" :key="index" :index="chat.id">
            <img :src="chat.avatar" class="avatar" alt="Avatar" />
            <span class="chat-name">{{ chat.name }}</span>
            <span class="unread-count">{{ chat.unread }}</span>
          </el-menu-item>
        </el-menu>
      </div>
      <div class="main">
        <div class="chat-header">
          <img :src="activeChatAvatar" class="avatar" alt="Avatar" />
          <span class="chat-name">{{ activeChatName }}</span>
        </div>
        <div class="chat-messages">
          <div v-for="(message, index) in activeChatMessages" :key="index" :class="getMessageClass(message)">
            <img :src="message.avatar" class="avatar" alt="Avatar" />
            <div class="message-content">{{ message.content }}</div>
          </div>
        </div>
        <div class="chat-input">
          <el-input
            v-model="inputMessage"
            placeholder="请输入消息"
            @keydown.enter="sendMessage"
            clearable
          >
            <el-button slot="append" @click="sendMessage">发送</el-button>
          </el-input>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        activeChat: null,
        chats: [
          {
            id: 1,
            name: '好友1',
            avatar: 'avatar-url',
            unread: 3,
            messages: [
              { sender: '好友1', content: '你好', isSelf: false },
              { sender: '自己', content: '你好，有什么需要帮助的吗？', isSelf: true },
              // ... more messages
            ]
          },
          {
            id: 2,
            name: '好友2',
            avatar: 'avatar-url',
            unread: 0,
            messages: [
              { sender: '好友1', content: '你好', isSelf: false },
              { sender: '自己', content: '你好，有什么需要帮助的吗？', isSelf: true },
              // ... more messages
            ]
          }
          // ... more chats
        ],
        inputMessage: ''
      };
    },
    computed: {
      activeChatMessages() {
        if (this.activeChat) {
          return this.activeChat.messages;
        }
        return [];
      },
      activeChatName() {
        if (this.activeChat) {
          return this.activeChat.name;
        }
        return '';
      },
      activeChatAvatar() {
        if (this.activeChat) {
          return this.activeChat.avatar;
        }
        return '';
      }
    },
    methods: {
      selectChat(chatId) {
        this.activeChat = this.chats.find(chat => chat.id === chatId);
      },
      getMessageClass(message) {
        return {
          'message-self': message.isSelf,
          'message-other': !message.isSelf
        };
      },
      sendMessage() {
        if (this.inputMessage.trim() === '') {
          return;
        }
  
        const newMessage = {
          sender: '自己',
          content: this.inputMessage,
          isSelf: true
        };
  
        if (this.activeChat) {
          this.activeChat.messages.push(newMessage);
        }
  
        this.inputMessage = '';
      }
    }
  };
  </script>
  
  <style scoped>
  .wechat-web {
    display: flex;
    height: 100vh;
  }
  
  .sidebar {
    width: 200px;
    background-color: #f5f5f5;
    border-right: 1px solid #ebebeb;
  }
  
  .sidebar-menu {
    padding-top: 20px;
  }
  
  .sidebar-menu .el-menu-item {
    display: flex;
    align-items: center;
  }
  
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
  }
  
  .chat-name {
    flex-grow: 1;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  
  .unread-count {
    background-color: #f56c6c;
    color: #fff;
    border-radius: 10px;
    padding: 2px 6px;
    font-size: 12px;
  }
  
  .main {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
  }
  
  .chat-header {
    display: flex;
    align-items: center;
    padding: 10px;
    background-color: #f5f5f5;
    border-bottom: 1px solid #ebebeb;
  }
  
  .chat-header .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
  }
  
  .chat-messages {
    flex-grow: 1;
    overflow-y: auto;
    padding: 10px;
  }
  
  .message-self {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 10px;
  }
  
  .message-other {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 10px;
  }
  
  .message-content {
    padding: 8px 12px;
    border-radius: 4px;
    background-color: #f5f5f5;
    word-wrap: break-word;
    max-width: 60%;
  }
  
  .chat-input {
    padding: 10px;
    background-color: #f5f5f5;
  }
  </style>
  