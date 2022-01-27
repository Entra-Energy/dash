<template>
  <table class="table table-striped">
    <thead>
      <tr>
        <th>DevID</th>
        <th>Status</th>
        <th>Power</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(dev,i) in all" :key="i">
         <td>{{ dev.id}}</td>
         <td>{{ dev.online }}</td>
         <td>{{ dev.pow }}</td>

      </tr>
     </tbody>
  </table>

</template>

<script>
import axios from 'axios';
export default {

  data() {
    return {
      all: [

        {
          "id":"sm-0001","pow":"", "online":"offline"
        },
        {
          "id":"sm-0002","pow":"", "online":"offline"
        },
        {
          "id":"sm-0003","pow":"", "online":"offline"
        },
        {
          "id":"sm-0004","pow":"", "online":"offline"
        }

    ],
      posts: [],
      errors: []
    };
  },

  methods: {
      getData() {
      try {
        axios
        .get(
          "http://64.225.100.195/api/online/"
        )
        .then(response => response.data.online.forEach(el=>{
            //this.posts.push(el)
            //console.log(el.dev)
            let found = this.all.find(element => element.id === el.dev)
            if (found)
            {
              found.pow = el.pow
              found.online = 'online'
            }

            //console.log(this.all[0].id)

        }) )
        //console.log(this.all)

      } catch (error) {
        //console.log(error);
      }
    },
  },
  created (){
    this.getData();



  },



};
</script>

<style scoped>

</style>
