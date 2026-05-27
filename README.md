# Poiyomi Shadow Cutoff Patcher

Poiyomi Pro の ShadowCaster パスに独立した Alpha Cutoff を追加するパッチャーです。  
透明マテリアルが影や SSAO に影響しないよう、Shadow パスのみ Cutoff を上書きできるようになります。

> **Note:** Poiyomi Pro の有効なライセンスが必要です。シェーダー本体はこのツールに含まれておらず、再配布もしていません。

---

## 使い方

### exe を使う

1. [Releases](../../releases) から `poiyomi_shadow_cutoff_patcher.exe` をダウンロード
2. exe を起動
3. `Poiyomi Pro.shader` をウィンドウにドロップ、またはクリックしてファイルを選択

シェーダーの場所（どちらか）：

```
<Unityプロジェクト>\Assets\_PoiyomiShaders\Shaders\10.0\Pro\Poiyomi Pro.shader
<Unityプロジェクト>\Packages\com.poiyomi.pro\_PoiyomiShaders\Shaders\10.0\Pro\Poiyomi Pro.shader
```

---

## パッチ後の使い方

Unity でマテリアルを開き、**Rendering Options** の **Shadow Caster Cutoff** セクションを有効にします。  
`Shadow Cutoff` を `1` に設定すると、そのマテリアルは影・SSAO に影響しなくなります。

---

## License

MIT
