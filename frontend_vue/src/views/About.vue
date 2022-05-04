<template>
  <div class="about">
    <div class="row">
      <div class="col-md-12">
          <Range @emit-it="handleChange" />
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <div class="pull-left">
          <Select @emit-sel="selectChange" />
      </div>
    </div>
   </div>



  </div>
</template>
<script>
// @ is an alias to /src
import Range from '@/components/Range.vue'
import Select from '@/components/Select.vue'

export default {
  name: 'About',
  components: {
    Range,
    Select
  },
  data() {
    return {
      dev : {},
      query:{},

    }
  },
  created() {
    let path = this.$route.path
    let title = this.$store.state.path
    let selected = this.$store.state.selected

    this.query['range'] = title
    if (selected){
      this.query['dev'] = selected
    }
    this.$router.push({path:path, query:this.query})

  },
  methods: {

    handleChange(payload){
      let path = this.$route.path
      // this.query = {
      //   "range": payload
      // }
      this.query['range'] = payload
      //console.log(this.query)
      this.$router.push({path:path, query:this.query})
    //  this.$router.push({path:path, query:{"range":payload.range, "dev": this.dev.dev}})
    //  console.log(payload)
  },
    selectChange(value)
    {
      let path = this.$route.path

      this.query["dev"] = value
      console.log(this.query)
      //let query = this.$route.query
      //this.dev = value

      //console.log(this.query)
      this.$router.push({path:path, query:this.query})

    }
  }
}
</script>

<style scoped>
.pull-left {
    float: left;
}
</style>
