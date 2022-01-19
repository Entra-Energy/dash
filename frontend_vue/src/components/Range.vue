<template>

  <ul>
    <li
      v-for="(item, index) in items"
      :key="item.index"
      :class="{ active: activeIndex === index }"
      @click="setActive(index)"
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
      items: [
        {
          id: 1,
          title: "Item #1",
        },
        {
          id: 2,
          title: "Item #2",
        },
        {
          id: 3,
          title: "Item #3",
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
  },
  methods: {
    setActive(index) {
      this.activeIndex = index;
      this.$store.commit('increment',this.activeIndex)

    },
    clickHandler(){

    }
  }

};
</script>

<style scoped>
.active {
  font-weight: bold;
}
</style>
