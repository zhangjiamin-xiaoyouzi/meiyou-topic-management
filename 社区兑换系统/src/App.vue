<template>
  <div class="exchange-app">
    <!-- 左侧菜单栏 -->
    <aside class="sidebar">
      <div class="brand">
        <span class="brand-badge">⌂</span>
        <span>兑换系统</span>
      </div>

      <div class="nav-list">
        <!-- 一级菜单（不可展开） -->
        <button
          v-for="item in primaryMenus"
          :key="item"
          class="nav-item"
          type="button"
        >
          <span class="nav-main">
            <span class="nav-icon"></span>
            <span class="nav-label">{{ item }}</span>
          </span>
        </button>

        <!-- 可展开菜单组：钱包管理 -->
        <div class="nav-group open">
          <button class="nav-item active" type="button">
            <span class="nav-main">
              <span class="nav-icon"></span>
              <span class="nav-label">钱包管理</span>
            </span>
            <span class="nav-arrow">⌃</span>
          </button>
          <div class="nav-sublist">
            <button
              v-for="item in walletMenus"
              :key="item.key"
              :class="['nav-subitem', { active: currentPage === item.key }]"
              type="button"
              @click="currentPage = item.key"
            >
              <span class="nav-main">
                <span class="nav-label">{{ item.label }}</span>
              </span>
            </button>
          </div>
        </div>

        <!-- 可展开菜单组：数据分析 -->
        <div class="nav-group">
          <button class="nav-item" type="button">
            <span class="nav-main">
              <span class="nav-icon"></span>
              <span class="nav-label">数据分析</span>
            </span>
            <span class="nav-arrow">⌄</span>
          </button>
        </div>

        <!-- 可展开菜单组：系统配置 -->
        <div class="nav-group">
          <button class="nav-item" type="button">
            <span class="nav-main">
              <span class="nav-icon"></span>
              <span class="nav-label">系统配置</span>
            </span>
            <span class="nav-arrow">⌄</span>
          </button>
        </div>
      </div>
    </aside>

    <!-- 右侧主内容区 -->
    <main class="content">
      <header class="topbar">
        <div class="breadcrumbs">
          <span>钱包管理</span>
          <span class="crumb-sep">›</span>
          <strong>{{ currentPageLabel }}</strong>
        </div>
      </header>
      <PrizeExchangeManagement />
    </main>
  </div>
</template>

<script>
import PrizeExchangeManagement from './components/PrizeExchangeManagement.vue'

export default {
  name: 'App',
  components: {
    PrizeExchangeManagement
  },
  data() {
    return {
      currentPage: 'prize',
      primaryMenus: [
        '兑换概览'
      ],
      walletMenus: [
        { key: 'prize', label: '奖品管理' },
        { key: 'order', label: '兑换订单' }
      ]
    }
  },
  computed: {
    currentPageLabel() {
      const walletItem = this.walletMenus.find(m => m.key === this.currentPage)
      return walletItem ? walletItem.label : '奖品管理'
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  width: 100%;
  height: 100%;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  color: #1f2430;
}

:global(*) {
  box-sizing: border-box;
}

.exchange-app {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 224px 1fr;
  --line: #e8e8ef;
  --brand: #e24b8d;
  --muted: #83889a;
}

/* ============ Sidebar ============ */
.sidebar {
  background: #fff;
  border-right: 1px solid var(--line);
}

.brand {
  height: 56px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 16px;
  border-bottom: 1px solid var(--line);
  font-size: 18px;
  font-weight: 600;
}

.brand-badge {
  width: 18px;
  height: 18px;
  border: 2px solid #2f3444;
  border-radius: 4px;
  font-size: 11px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.nav-list {
  padding: 8px;
  display: grid;
  gap: 2px;
}

.nav-item,
.nav-subitem {
  width: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 12px 10px;
  border: none;
  border-radius: 12px;
  color: #1f2430;
  background: none;
  text-align: left;
  cursor: pointer;
  font-family: inherit;
  font-size: 14px;
  transition: background 0.15s;
}

.nav-item:hover,
.nav-subitem:hover {
  background: rgba(226, 75, 141, 0.04);
}

.nav-item.active,
.nav-subitem.active {
  color: var(--brand);
  background: linear-gradient(90deg, rgba(226, 75, 141, 0.08), rgba(226, 75, 141, 0));
}

.nav-item.active::before,
.nav-subitem.active::before {
  content: '';
  position: absolute;
  left: 0;
  width: 3px;
  height: 26px;
  border-radius: 999px;
  background: var(--brand);
}

.nav-main {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-icon {
  width: 14px;
  height: 14px;
  border: 1.6px solid currentColor;
  border-radius: 2px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.nav-arrow {
  color: #99a1b3;
  font-size: 12px;
}

.nav-sublist {
  padding-left: 12px;
}

.nav-subitem {
  padding-left: 32px;
}

/* ============ Content Area ============ */
.content {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f7;
}

.topbar {
  height: 56px;
  display: flex;
  align-items: center;
  padding: 0 24px;
  background: #fff;
  border-bottom: 1px solid var(--line);
  flex-shrink: 0;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--muted);
}

.breadcrumbs strong {
  color: #1f2430;
  font-weight: 600;
}

.crumb-sep {
  color: #c0c4cc;
}
</style>

