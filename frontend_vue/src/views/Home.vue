<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <Range @emit-it="handleChange"/>

    <Table />
    <LineCharts />

  </div>
</template>

<script>

// @ is an alias to /src

import Range from '@/components/Range.vue'
import Table from '@/components/Table.vue'
import LineCharts from '@/components/LineCharts.vue'


export default {
  name: 'Home',
  components: {
    Range,
    Table,
    LineCharts,
  },
  data() {
    return {

    }
  },
  created (){
    let path = this.$route.path
    let title = this.$store.state.path
    this.$router.push({path:path, query:{"range":title}})


  },

  methods: {
    handleChange(payload){
      let path = this.$route.path

      this.$router.push({path:path, query:{"range":payload}})

    }


  },
}
</script>
