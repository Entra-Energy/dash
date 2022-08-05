
  <template>
        <div class='row'><div class='col'><Range @emit-it="handleChange"/></div></div>
        <div class='row'><div class='col'><ArisCharts :query="query" /></div></div>
      
  </template>


<script>
  import Range from '@/components/Range.vue'
  import ArisCharts from '@/components/ArisCharts.vue'


  export default {
    name: 'Producer',
    components: {
      Range,
      ArisCharts
    },
    data() {
      return {
        query:"today",
        rangeTitle:'',
      }
    },
    created (){
      let rangeIndex = this.rangeTitle
      let path = this.$route.path
      this.$router.push({path:path, query:{"range":rangeIndex}})

    },
    methods: {
      handleChange(payload){
        let path = this.$route.path
        this.query = payload
        this.$router.push({path:path, query:{"range":payload}})
      }
    },
    watch: {
      '$store.state.dash_init': {
        immediate: true,
        handler() {
            this.rangeTitle = this.$store.state.dash_init;
        }
      }
    },
  }

</script>
