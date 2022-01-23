<template>

  <ul>
    <li
      v-for="(item, index) in items"
      :key="item.index"
      :class="{ active: activeIndex === index }"
      @click="setActive(index, item.title);clickHandler()"
    >
      <slot :item="item">
        <p>
          {{ item["title"] }}
          {{ activeI }}
        </p>
      </slot>
    </li>
  </ul>
</template>


<script>

export default {

  data() {
    return {
      activeIndex: 0,
      title: 'day',
      items: [
        {
          id: 1,
          title: "day",
        },
        {
          id: 2,
          title: "month",
        },
        {
          id: 3,
          title: "year",
        },
      ],
    };
  },
  props: {
    activeI: {
      type: Number,
    },
  },
  created (){

      this.activeIndex = this.$store.state.count
      //this.title = this.$store.state.path

      //let path = this.$route.path
      //this.$router.push({path:path, query:{"range":this.title}})
      //console.log(this.title)

  },
  methods: {
    setActive(index, title) {
      this.activeIndex = index;
      this.$store.commit('increment',index)
      this.$emit("emit-it", title)
      // let path = this.$route.path
      // this.$router.push({path:path, query:{"range":title}})
      //
      this.$store.commit('setPath', title)
    },
    clickHandler(index){
    //  let query = {"range":index}
    //  this.$emit("emit-it", query)
  },

  }

};
</script>

<style scoped>
.active {
  font-weight: bold;
}
</style>
