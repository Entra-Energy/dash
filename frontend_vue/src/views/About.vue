<template>
  <div class="about">
    <h1>This is an about page</h1>
    <Range />
  </div>
</template>
<script>
// @ is an alias to /src
import Range from '@/components/Range.vue'

export default {
  name: 'About',
  components: {
    Range
  },
  data() {
    return {
      
    }
  },
}
</script>
