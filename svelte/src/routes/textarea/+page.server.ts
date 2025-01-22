export async function load({ fetch, url }) {
    let noJS  = !!url.searchParams.get("noJS")

    async function minimalRespponse() {
        let resp = await fetch(`https://loripsum.net/generate.php?p=1&l=short`)
        let respText = await resp.text()
        return respText
    }

    async function biggerRespponse() {
        let resp = await fetch(`https://loripsum.net/generate.php?p=1&l=medium`)
        let respText = await resp.text()
        return respText
    }

    async function hugeResponse() {
        let resp = await fetch(`https://loripsum.net/generate.php?p=5000&l=long`)
        let respText = await resp.text()
        return respText
    }

    const [minimalData, biggerData] =
    await Promise.all([
        await minimalRespponse(),
        await biggerRespponse()
    ]);

    return {
        hugeData: noJS ? await hugeResponse() : hugeResponse(),
        minimalData,
        biggerData
    }
}
