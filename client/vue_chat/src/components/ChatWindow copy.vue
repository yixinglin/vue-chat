<template>
  <div class="wechat-web">
    <div class="sidebar">
      <el-menu default-active="activeChat" class="sidebar-menu" @select="selectChat">
        <el-menu-item v-for="(chat, index) in chats" :key="index" :index="chat.id">
          <img :src="chat.avatar" class="avatar" alt="Avatar" />
          <span class="chat-name">{{ chat.name }}</span>
        </el-menu-item>
      </el-menu>
      <el-input v-model="newContact" placeholder="请输入好友名称" clearable class="add-contact-input"
        @keydown.enter="addContact">
        <el-button slot="append" @click="addContact">添加</el-button>
      </el-input>
    </div>
    <div class="main">
      <div class="chat-header">
        <img :src="activeChatAvatar" class="avatar" alt="Avatar" />
        <span class="chat-name-header">{{ activeChatName }}</span>
      </div>
      <div class="chat-messages">
        <div v-for="(message, index) in activeChatMessages" :key="index" :class="getMessageClass(message)">
          <!-- <img :src="message.avatar" class="avatar" alt="Avatar" /> -->
          <div class="message-content">{{ message.content }}</div>
        </div>
      </div>
      <div class="chat-input">
        <el-input v-model="inputMessage" placeholder="请输入消息" @keydown.enter="sendMessage" clearable></el-input>
        <el-button @click="sendMessage" :loading="!submitEnabled">发送</el-button>
      </div>
    </div>
  </div>
</template>
  
<script>

import axios from 'axios';

export default {
  data() {
    return {
      activeChat: null,
      submitEnabled: true,  // 发送消息按钮
      chats: [
        {
          id: '1',
          name: '小明',
          avatar: 'avatar.jpg',
          messages: [
            { sender: '好友1', content: '你好', isSelf: false },
            { sender: '自己', content: '你好，有什么需要帮助的吗？', isSelf: true },
            // ... more messages
          ]
        },
        // ... more chats
      ],
      inputMessage: '',
      newContact: ''
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
      return 'blank.png';
    }
  },
  methods: {
    selectChat(chatId) {
      this.activeChat = this.chats.find(chat => chat.id === chatId);
      console.log(this.activeChat.id)
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
        this.sendChatMessage(newMessage.content);
      }

      this.inputMessage = '';
    },
    addContact() {
      if (this.newContact.trim() === '') {
        return;
      }

      const newChat = {
        id: (this.chats.length + 1).toString(),
        name: this.newContact,
        avatar: 'avatar.jpg',
        messages: []
      };

      this.chats.push(newChat);
      this.newContact = '';
    },
    //向服务端发送对话消息
    sendChatMessage(content) {
      console.log(this.activeChat.name);
      this.submitEnabled = false;
      var post_body = {
        "bot_name": this.activeChat.name,
        "temperature": 0.7,
        "sys_prompt": "You are a teacher who teaches German.",
        "prompt": content
      }

      const currentChat = this.activeChat;
      axios.post("/chat3_5", post_body).then(response => {
        console.log( response.data);
        // 机器人的回答
        var c = { sender: currentChat.name, content:  response.data.content, isSelf: false };
        currentChat.messages.push(c);
      }).catch(error => {
        console.log(error);
      }).finally (()=> {
        this.submitEnabled = true;
      })
    },

    // 从服务端获取所有的对话
    convertConversationsAPIFormat(data) {
      const conversations = data['data'];
      this.chats = []
      for (let index = 0; index < conversations.length; index++) {
        const bot = conversations[index];
        console.log(bot);
        var messages = [];
        bot.history.forEach(element => {
          if (element.role == 'user') {
            messages.push({ sender: '自己', content: element.content, isSelf: true });
          }
          if (element.role == 'assistant') {
            messages.push({ sender: bot.bot_name, content: element.content, isSelf: false });
          }
          if (element.role == 'system') {
            messages.push({ sender: '系统', content: element.content, isSelf: true });
          }
        });

        var contact = {
          id: (index + 1).toString(),
          name: bot.bot_name,
          avatar: 'avatar.jpg',
          messages: messages
        };
        this.chats.push(contact);


      }
      // contact = {
      //     id: '1',
      //     name: '小明',
      //     avatar: 'avatar.jpg',
      //     messages: [
      //       { sender: '好友1', content: '你好', isSelf: false },
      //       { sender: '自己', content: '你好，有什么需要帮助的吗？', isSelf: true },
      //       // ... more messages
      //     ]
      // }
    },
    fetchConversations() {
      axios.get("chat3_5/all_conversations")
        .then(response => {
          console.log(response.data);
          this.convertConversationsAPIFormat(response.data);
        })
        .catch(error => {
          console.log(error);
        })
    }

  },
  mounted() {
    console.log("Mounted");
    this.fetchConversations();
    
  }
};
</script>
  

<style scoped>
.wechat-web {
  display: flex;
  height: 90vh;
  width: 70vw;
}

.sidebar {
  width: 250px;
  background-color: #f5f5f5;
  border-right: 1px solid #ebebeb;
  padding-bottom: 50px;
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
  text-align: left;
}

.chat-name-header {
  flex-grow: 1;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  text-align: center;
  font-size: 20px;
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
  text-align: left;
}

.chat-input {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f5f5f5;
}

.chat-input .el-input {
  flex-grow: 1;
  margin-right: 10px;
}
</style>
  