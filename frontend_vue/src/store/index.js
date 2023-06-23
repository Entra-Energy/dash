import { createStore } from 'vuex'

export default createStore({
  state: {
    count:'today',
    path: 'today',
    selected:'',
    zoom: {},
    checked_devs: '',
    dash_init: 'today',
    client_init: 'today',
    producer_init: 'today',
    dash_zoom: {},
    client_zoom: '',
    monthData:[],
    allDevs:[],
    allIds:[],
    allForecastIds:[],
    capacity:[],
    resolution:1
   
    
  },
  mutations: {
    increment (state, n) {
      state.count = n
    },
    setPath (state,query)
    {
      state.path = query
    },
    setSelect (state, select)
    {
      state.selected = select
    },
    setZoom (state, myZoom)
    {
      state.zoom = myZoom
    },
    setChecked (state, checked_state)
    {
      state.checked_devs = checked_state
    },
    initDash(state,dash)
    {
      state.dash_init = dash
    },
    initClient(state, client)
    {
      state.client_init = client
    },
    initProducer(state, prod)
    {
      state.producer_init = prod
    },
    dashZoomInit(state, dashZ)
    {
      state.dash_zoom = dashZ
    },
    clientZoomInit(state, clientZ)
    {
      state.client_zoom = clientZ
    },
    loadMonthData(state, month)
    {
      state.monthData = month
    },
    createAllDevs(state, all)
    {
      state.allDevs = all
    },
    createAllIds(state, ids)
    {
      state.allIds = ids
    },
    createAllForecastIds(state,forecastIds)
    {
        state.allForecastIds = forecastIds
    },
    setCapacity(state, capa)
    {
      state.capacity = capa
    },
    setResolution(state, res)
    {
      state.resolution = res
    },


  },
  actions: {
  },
  modules: {
  }
})
