<template>
  <div class="wechat-web">
    <div class="sidebar">
      <el-menu default-active="activeChat" class="sidebar-menu" @select="selectChat">
        <el-menu-item v-for="(chat, index) in chats" :key="index" :index="chat.id">
          <img :src="chat.avatar" class="avatar" alt="Avatar" />
          <span class="chat-name">{{ chat.name }}</span>
          <i class="el-icon-delete" @click.stop="deleteContact(chat)"></i>
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
          <div class="message-content">{{ message.content }}</div>
        </div>
      </div>
      <div class="chat-input">
        <!-- <el-input v-model="inputMessage" placeholder="请输入消息" @keydown.enter="sendMessage" clearable></el-input> -->
        <el-input type="textarea" :row="2" v-model="inputMessage" placeholder="请输入消息" @keydown.enter="sendMessage"
          clearable></el-input>
        <el-button @click="sendMessage" :loading="!submitEnabled">发送</el-button>
      </div>
    </div>

    <!-- <div class="control-panel">
      <span>Temperature</span>
      <el-slider :v-model="0.7" :format-tooltip="formatTooltip" />
    </div> -->
  </div>

</template>


<script>
import axios from 'axios';
// import marked from 'marked';

export default {
  data() {
    return {
      activeChat: null,
      submitEnabled: true,
      listAvatar: ["panda.png", "bear.png", "cat.png", "chicken.png", "dog.png", "rabbit.png", 'woman.png', 'woman2.png', 'man.png', 'astronaut.png'],
      chats: [
        {
          id: '1',
          name: '小明',
          avatar: 'panda.png',
          messages: [
            { sender: '好友1', content: '你好', isSelf: false },
            { sender: '自己', content: '你好，有什么需要帮助的吗？', isSelf: true },
          ]
        },
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

      const aIndex = this.chats.length % this.listAvatar.length;

      const newChat = {
        id: (this.chats.length + 1).toString(),
        name: this.newContact,
        avatar: this.listAvatar[aIndex],
        messages: []
      };

      this.chats.push(newChat);
      this.newContact = '';
    },
    deleteContact(chat) {
      const index = this.chats.indexOf(chat);
      if (index !== -1) {
        this.chats.splice(index, 1);
        if (this.activeChat === chat) {
          this.activeChat = null;
        }
      }
    },
    sendChatMessage(content) {
      this.submitEnabled = false;
      this.$message({ message: '回答中...' });
      var post_body = {
        "bot_name": this.activeChat.name,
        "temperature": 0.7,
        "sys_prompt": "You are a helpful assistant.",
        "prompt": content
      }

      const currentChat = this.activeChat;
      axios.post("/chat3_5", post_body).then(response => {
        var c = { sender: currentChat.name, content: response.data.content, isSelf: false };
        currentChat.messages.push(c);
      }).catch(error => {
        console.log(error);
      }).finally(() => {
        this.submitEnabled = true;
        this.$message({ message: '回答完毕！', type: 'success' });
      })
    },
    convertConversationsAPIFormat(data) {
      const conversations = data['data'];
      this.chats = [];
      for (let index = 0; index < conversations.length; index++) {
        const bot = conversations[index];
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

        const aIndex = this.chats.length % this.listAvatar.length;
        var contact = {
          id: (index + 1).toString(),
          name: bot.bot_name,
          avatar: this.listAvatar[aIndex],
          messages: messages
        };
        this.chats.push(contact);
      }
    },
    fetchConversations() {
      axios.get("chat3_5/all_conversations")
        .then(response => {
          this.convertConversationsAPIFormat(response.data);
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  mounted() {
    this.fetchConversations();
  }
};
</script>
<style scoped>
.wechat-web {
  display: flex;
  height: 80vh;
  /* width: 70vw; */
}

.sidebar {
  width: 200px;
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
  border-radius: 20%;
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
  border-radius: 20%;
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

/* .control-panel {
  flex-direction: row;
  background-color: #f5f5f5;
} */

</style>
