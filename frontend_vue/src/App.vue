<template>
  <div class='wrapper'>
    <div class="login" v-if="hideLogin"><Login @emit-it="usrName"/></div>
    <div class="sidebar" v-if="isAuth">
    <sidebar-menu :menu="menu" :collapsed="collapsed" :disableHover="disableHover" :hideToggle="hideToggle" />
    </div>
    <div class='main-panel'>
      <nav class='navbar navbar-expand-lg navbar-absolute navbar-transparent'>          
        <img src="@/assets/logo.png" />         
      </nav>
      <div class='content' v-if="isAuth">
        <router-view/>
      </div>
      <footer class='footer'></footer>
    </div>
  </div>
</template>
<script>
import Login from '@/components/Login.vue'
import { is } from '@babel/types';
import mqtt from 'mqtt';
import { coords } from './coord.js'
export default {
  components: {
    Login,
  },
    data() {
      return {
        //mqtt
        connection: {
          protocol: "ws",
          host: "159.89.103.242",
          // ws: 8083; wss: 8084
          port: 9001,
          endpoint: "/mqtt",
          // for more options, please refer to https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options
          clean: true,
          connectTimeout: 30 * 1000, // ms
          reconnectPeriod: 4000, // ms
          clientId: "emqx_vue_" + Math.random().toString(16).substring(2, 8),
          // auth
          //username: "emqx_test",
          //password: "emqx_test",
        },
        subscription: {
          topic: "ping/+",
          qos: 0,
        },
        client: {
          connected: false,
        },
        subscribeSuccess: false,
        connecting: false,
        retryTimes: 0,

        menu: [
          {
            header: 'Energy Dashboard',
            hiddenOnCollapse: true
          },
          {
            href: '/',
            title: 'Dashboard',
            icon: 'fa-solid fa-chart-line',

          },
          {
            href: '/client',
            title: 'Client',
            icon: 'fa-solid fa-microchip',

          },
          // {
          //   href: '/analytics',
          //   title: 'Analytics',
          //   icon: 'fa-solid fa-microchip',

          // },
          
          {
            href: '/flexi',
            title: 'Flexability',
            icon: 'fa-solid fa-dice-d20',

          },
          {
            href: '/grid',
            title: 'Flexability Simulate',
            icon: 'fa-solid fa-sliders',

          },
          {
            href: '/system',
            title: 'System',
            icon: 'fa-solid fa-list-check',

          },
          {
            href: '/producer',
            title: 'Producer',
            icon: 'fa-solid fa-solar-panel',

          },
          {
            href: '/storage',
            title: 'Storage',
            icon: 'fa-solid fa-battery-quarter',

          },

        ],
        sm_coeff: [{"sm-0001":120},{"sm-0002":320},{"sm-0003":400},{"sm-0004":200},{"sm-0006":200},{"sm-0008":200},{"sm-0009":80},{"sm-0010":60},{"sm-0011":60},{"sm-0015":60},{"sm-0016":250}],  
     
        collapsed: false,
        disableHover: true,
        hideToggle: true,
        all:[],
        isAuth: false,
        hideLogin: true
      }
    },

    methods: {
    initData() {
      this.client = {
        connected: false,
      };
      this.retryTimes = 0;
      this.connecting = false;
      this.subscribeSuccess = false;
    },
    handleOnReConnect() {
      this.retryTimes += 1;
      if (this.retryTimes > 5) {
        try {
          this.client.end();
          this.initData();
          this.$message.error("Connection maxReconnectTimes limit, stop retry");
        } catch (error) {
          this.$message.error(error.toString());
        }
      }
    },
    doSubscribe() {
      const { topic, qos } = this.subscription
      this.client.subscribe(topic, { qos }, (error, res) => {
        if (error) {
          console.log('Subscribe to topics error', error)
          return
        }
        this.subscribeSuccess = true
        console.log('Subscribe to topics res', res)
      })
    },

    createConnection() {
        try {
          this.connecting = true;
          const { protocol, host, port, endpoint, ...options } = this.connection;
          const connectUrl = `${protocol}://${host}:${port}${endpoint}`;
          this.client = mqtt.connect(connectUrl, options);
          if (this.client.on) {
            this.client.on("connect", () => {
              this.connecting = false;
              console.log("Connection succeeded!");
            });
            this.client.on("reconnect", this.handleOnReConnect);
            this.client.on("error", (error) => {
              console.log("Connection failed", error);
            });
            this.client.on("message", (topic, message) => {
              let parser = JSON.parse(`${message}`)              
              let dev = topic.split("/")[1]
              let pow = parser.payload.power
              this.sm_coeff.forEach(el=>{
                let keyId = Object.keys(el);                
                if(keyId[0] === dev){
                  pow *=el[keyId[0]]
                }
              })
              let devObj = {
                "dev":dev,
                "pow":pow.toFixed(2),
                "ready":parser.payload.gridReady,
                "providing":parser.payload.providing                
              }
            // console.log(devObj.dev)
              let found = this.all.find(element => element.id === devObj.dev)
              if(found){              
                found.pow = devObj.pow
                found.providing = devObj.providing
                found.online = 'online'
                found.ready = devObj.ready
                found.customer = parser.payload.blynkName
                if (found.ready == 1)
                {
                  if (found.providing == 0)
                  {
                  found.online = 'ready'
                  }
                  else if (found.providing == 1)
                  {
                    found.online = 'providing'
                  }
                }
                else if (found.ready == 0)
                {
                  found.online = 'not-ready'
                }
                else{
                  found.online = 'offline'
                }
                
              }
              this.$store.commit('createAllDevs', this.all)
              //console.log(this.all)
            
            });
          }
        } catch (error) {
          this.connecting = false;
          console.log("mqtt.connect error", error);
        }
    },

    usrName(payload){
      if(payload.username === "admin" && payload.pass === "admin")
      {
        this.isAuth = true
        this.hideLogin = false
      }
    },

      createAllDevs(){          
        let prefix = 'sm-'          
        for(let i = 0; i <= 30; i++)
        {
          let new_dev = prefix+'000'+i;            
          if (i >= 10){
            new_dev = prefix + '00' + i;              
          }                         
          this.all.push({"id":new_dev,"online":"offline"})
        }          
        let ids = []
        let forecastIds = []
        this.all.forEach(el=>{
          for(let i=0;i<coords.length;i++)
          {
            let keyId = Object.keys(coords[i]); 
            if(el.id === keyId[0]){
              el.lat = coords[i][keyId].lat
              el.long = coords[i][keyId].long 
              //continue;             
            }
            
          }
          ids.push(el.id)
          forecastIds.push(el.id + 'F')
        })
        // this.$store.commit('createAllDevs', this.all)
        this.$store.commit('createAllIds', ids)
        this.$store.commit('createAllForecastIds', forecastIds)
        console.log(this.all)
    },

      detectIt(){

        if (this.$screen.width < 1000)
        {
          this.collapsed = true
        }
        else {
          this.collapsed = false
        }
      },

    },
    created () {  
     
     this.createAllDevs()
     this.detectIt()
     this.createConnection();
     this.doSubscribe();
     
    },
    computed: {

    },
  }

</script>
<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {

  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
.v-sidebar-menu {
    background-color: #782686 !important;
    top: 53px !important;
    bottom: 37px !important;
    border-bottom-right-radius: 0.2857rem;
    border-top-right-radius: 0.2857rem;
}
/*****/
.sidebar {
  height: calc(100vh - 90px);
  width: 197px;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1;
  display: block;
  box-shadow: 0 0 45px 0 rgb(0 0 0 / 60%);
  margin-top: 52px;
  margin-left: 20px;
  border-radius: 5px;
  transition: .5s cubic-bezier(.685,.0473,.346,1);
}
.main-panel{
  position: relative;
  float: right;
  width: 100%;
  min-height: 100vh;
  border-top: 2px solid #e14eca;
  background: linear-gradient(#1e1e2f,#1e1e24);
}
.main-panel>.navbar {
    margin-bottom: 0;
}
.main-panel>.content {
    //padding: 0px 30px 30px 280px;
    padding: 0px 8px 30px 233px;
    min-height: calc(100vh - 70px);
}
.v-sidebar-menu.vsm_expanded {
  max-width:215px !important;
}
@media screen and (max-width: 991px){
.main-panel .content {
    padding-left: 100px;
}
.sidebar {
    position: fixed;
    display: block;
    top: 0;
    height: 100%;
    max-width: 68px;
    right: auto;
    left: 0;
    margin: 0;
    border-radius: 0;
    z-index: 1032;
    visibility: visible;
    overflow-y: visible;
    padding: 0;
//     -webkit-transition: .5s cubic-bezier(.685,.0473,.346,1);
//     transition: .5s cubic-bezier(.685,.0473,.346,1);
//      // -webkit-transform: translate3d(-100px,0,0);
//      // transform: translate3d(-100px,0,0);
//      -webkit-transform: width(70px);
//      transform: width(70px);
 }
}
.navbar{
padding-bottom: 0.625rem;
min-height: 53px;
/*border-bottom: 1px solid #ddd;*/
}
.v-sidebar-menu .vsm--header {
    font-size: 16px;
    font-weight: 600;
    padding: 6px 15px;
    text-transform: none;
    white-space: nowrap;
    border-top-right-radius: 0.2857rem;
    border-bottom: 1px solid;
}
.v-sidebar-menu .vsm--mobile-bg {
  background: none !important;
}
.v-sidebar-menu .vsm--link_level-1 .vsm--icon {
    background: none !important;
}

.v-sidebar-menu .vsm--link {
  font-size: 15px !important;
}

.v-sidebar-menu .vsm--link_level-1.vsm--link_active{
  background: #550a61;
}
// .navy {
//     text-align: center;
//     margin: 0 auto;
// }
</style>
