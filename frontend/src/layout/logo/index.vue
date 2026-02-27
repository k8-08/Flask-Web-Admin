<template>
  <div class="layout-logo" v-if="setShowLogo" @click="onThemeConfigChange">
    <span class="layout-logo-text">{{ themeConfig.globalTitle }}</span>
  </div>
  <div class="layout-logo-size" v-else @click="onThemeConfigChange">
    <span class="layout-logo-mini">F</span>
  </div>
</template>

<script setup lang="ts" name="layoutLogo">
import {computed} from 'vue';
import {storeToRefs} from "/@/stores";
import {useThemeConfig} from '/@/stores/themeConfig';
import { logos } from '/@/config/assets';

// 定义变量内容
const storesThemeConfig = useThemeConfig();
const {themeConfig} = storeToRefs(storesThemeConfig);

// 设置 logo 的显示。classic 经典布局默认显示 logo
const setShowLogo = computed(() => {
  let {isCollapse, layout} = themeConfig.value;
  return !isCollapse || layout === 'classic' || document.body.clientWidth < 1000;
});
// 获取logo
// const getLogo = computed(() => { ... }); // 已改为文字显示，不再需要图片

// logo 点击实现菜单展开/收起
const onThemeConfigChange = () => {
  if (themeConfig.value.layout === 'transverse') return false;
  themeConfig.value.isCollapse = !themeConfig.value.isCollapse;
};
</script>

<style scoped lang="scss">
.layout-logo {
  width: 220px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: rgb(0 21 41 / 2%) 0px 1px 4px;
  color: var(--el-color-primary);
  font-size: 16px;
  cursor: pointer;
  animation: logoAnimation 0.3s ease-in-out;

  span {
    white-space: nowrap;
    display: inline-block;
  }

  &:hover {
    span {
      color: var(--color-primary-light-2);
    }
  }

  &-medium-img {
    max-width: 180px;
    max-height: 40px;
    margin-right: 5px;
    object-fit: contain;
  }

  .layout-logo-text {
    font-size: 16px;
    font-weight: 700;
    color: #fff;
    letter-spacing: 1px;
    white-space: nowrap;
  }
}

.layout-logo-size {
  width: 100%;
  height: 50px;
  display: flex;
  cursor: pointer;
  animation: logoAnimation 0.3s ease-in-out;

  &-img {
    max-width: 32px;
    max-height: 32px;
    margin: auto;
    object-fit: contain;
  }

  &:hover {
    img {
      animation: logoAnimation 0.3s ease-in-out;
    }
  }
}
</style>
