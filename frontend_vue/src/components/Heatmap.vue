<template>
    <vue-google-heatmap :points="points"
                        
                        :height="350"
                        :initial-zoom=10
                        :lat="42.6443910020"
                        :lng="23.3731367"
                        :mapType ='satellite'
                        :radius=400
                        :maxIntensity=1
                        :saturation= -100 />
  </template>

<script>
export default {
  data() {
    return {
      points: [
        {lat: 42.644, lng:23.373136753287096},
        {lat: 42.642, lng:23.373136753287096},
        {lat: 42.645, lng:23.373136753287096},
        {lat: 42.644, lng:23.343,weight: 22},
        {lat: 42.643, lng:23.323,weight: 20},
        {lat: 42.641, lng:23.366,weight: 19},
        {lat: 42.643, lng:23.377,weight: 10},
        {lat: 42.641, lng:23.333,weight: 2},
        {lat: 42.640, lng:23.371,weight: 2},
        {lat: 42.649, lng:23.378,weight: 2},
        {lat: 42.650, lng:23.373},
        {lat: 42.648, lng:23.373},
        {lat: 42.649, lng:23.383},
        {lat: 42.644, lng:23.363136753287096},
        {lat: 42.642, lng:23.363136753287096},
        {lat: 42.645, lng:23.373136753287096},
        {lat: 42.644, lng:23.313,weight: 22},
        {lat: 42.643, lng:23.323,weight: 20},
        {lat: 42.641, lng:23.336,weight: 19},
        {lat: 42.643, lng:23.347,weight: 10},
        {lat: 42.641, lng:23.353,weight: 2},
        {lat: 42.640, lng:23.361,weight: 2},
        {lat: 42.649, lng:23.378,weight: 2},
        {lat: 42.650, lng:23.383},
        {lat: 42.648, lng:23.383},
        {lat: 42.649, lng:23.393},
        {lat: 42.644, lng:23.363136753287096},
        {lat: 42.642, lng:23.363136753287096},
        {lat: 42.645, lng:23.373136753287096},
        {lat: 42.644, lng:23.313,weight: 22},
        {lat: 42.643, lng:23.323,weight: 20},
        {lat: 42.641, lng:23.336,weight: 19},
        {lat: 42.643, lng:23.347,weight: 10},
        {lat: 42.641, lng:23.353,weight: 2},
        {lat: 42.640, lng:23.361,weight: 2},
        {lat: 42.649, lng:23.378,weight: 2},
        {lat: 42.650, lng:23.383},
        {lat: 42.648, lng:23.383},
        {lat: 42.649, lng:23.393}
      ]
    }
  }
}
</script>