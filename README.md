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

## Credits

Shadow Caster Cutoff の仕組みは [lilToon](https://github.com/lilxyzw/lilToon) の Subpass Cutoff 機能を参考にしています。

---

## License

MIT License

Copyright (c) 2025 qsyi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
