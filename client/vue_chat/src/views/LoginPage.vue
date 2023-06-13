<template>
    <div class="login-page">
        <div class="login-container">
            <el-form ref="loginForm" :model="form" class="login-form">
                <h2 class="login-title">登录</h2>
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input type="password" v-model="form.password" placeholder="请输入密码"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="login">登录</el-button>
                </el-form-item>
            </el-form>
        </div>
                                                                         
        <div class="block">
            <span style="color:antiquewhite"> 温度 </span>
            <el-slider v-model="temperature" :step="1" :format-tooltip="formatTooltip" vertical height="200px">
            </el-slider>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
export default {
    'name': 'LoginPage',
    data() {
        return {
            temperature: 50,
            form: {
                username: '',
                password: ''
            },
            request_headers: { "Content-Type": "application/json;charset=utf-8" }
        };
    },
    methods: {
        login() {
            // 在这里执行登录验证的逻辑
            // 比较输入的用户名和密码与预设的合法值
            axios.post("/login", this.form, { headers: this.request_headers }
            ).then(resp => {
                if (resp.data.status == 200) {
                    // 登录成功，执行相应的操作
                    alert('登录成功');
                    let token = {
                        "name": this.form.username,
                        "time": new Date().getTime()
                    }
                    localStorage.setItem("token", JSON.stringify(token));
                    localStorage.setItem("temperature", this.formatTooltip(this.temperature))
                    this.$router.push("/")
                } else {
                    // 登录失败，显示错误信息
                    alert('用户名或密码错误');
                }
            })

        },
        formatTooltip(val) {
            return (0.4+0.006*val).toFixed(2); 
        }
    }
};
</script>
  
<style scoped>
.login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    background-size: cover;
    background-position: center;
}

.login-container {
    width: 320px;
    padding: 20px;
    border-radius: 8px;
    background-color: rgba(255, 255, 255, 0.8);
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.login-form {
    margin-bottom: 20px;
}

.login-title {
    text-align: center;
    margin-bottom: 20px;
    color: #fff;
    font-size: 24px;
    letter-spacing: 2px;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.el-form-item__label {
    color: #fff;
}

.el-input__inner,
.el-button {
    color: #fff;
    background-color: #3f51b5;
    border-color: #3f51b5;
}

.el-input__inner::placeholder {
    color: #ccc;
}

.el-input__inner:hover,
.el-button:hover {
    background-color: #2a3f8a;
    border-color: #2a3f8a;
}

.el-button:active {
    background-color: #1c285c;
    border-color: #1c285c;
}

.el-button:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(63, 81, 181, 0.4);
}
</style>
  