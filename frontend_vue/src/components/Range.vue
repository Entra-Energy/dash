<template>

  <div class="mt-3">
<ul class="list-group list-group-horizontal">
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
    <!-- <ul>

    </ul> -->
  </div>

</template>


<script>

export default {

  data() {
    return {
      activeIndex: 0,
      title: 'today',
      items: [
        {
          id: 1,
          title: "today",
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
      this.title = this.$store.state.path

      let path = this.$route.path
      this.$router.push({path:path, query:{"range":this.title}})
      //console.log(this.title)

  },
  methods: {
    setActive(index, title) {
      this.activeIndex = index;
      this.$store.commit('increment',index)
      this.$emit("emit-it", title)
      let path = this.$route.path
      this.$router.push({path:path, query:{"range":title}})
      //console.log(title)
      this.$store.commit('setPath', title)
    },
    clickHandler(index){
     let query = {"range":index}
     this.$emit("emit-it", query)
  },

  }

};
</script>

<style scoped>
.active {
  font-weight: bold;
}
</style>
