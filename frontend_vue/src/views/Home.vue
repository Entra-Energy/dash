<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <Range />
    <HelloWorld msg="Welcome to Your Vue.js App"/>
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
}
</script>
