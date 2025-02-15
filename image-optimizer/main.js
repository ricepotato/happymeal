console.log("Hello World");

/**
 * image 경로를 받아서 이미지를 sharp 라이브러리를 사용해서 128x128 로 변환하는 함수
 * 이미지의 비율을 유지한다. 이미지가 가로나 세로로 더 길면 crop 한다
 */

const sharp = require("sharp");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

/**
 * 파일의 해시값을 계산하는 함수
 * @param {string} filePath - 해시를 계산할 파일 경로
 * @returns {Promise<string>} 파일의 해시값
 */
async function calculateFileHash(filePath) {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash("sha256");
    const stream = fs.createReadStream(filePath);

    stream.on("data", (data) => hash.update(data));
    stream.on("end", () => resolve(hash.digest("hex")));
    stream.on("error", (error) => reject(error));
  });
}

/**
 * 이미지를 128x128 크기로 리사이즈하는 함수
 * @param {string} inputPath - 원본 이미지 경로
 * @param {string} outputPath - 저장할 이미지 경로
 * @returns {Promise} 이미지 처리 결과를 담은 Promise
 */
function resizeImage(inputPath, outputPath) {
  return sharp(inputPath)
    .resize(128, 128, {
      fit: "cover", // 이미지를 꽉 채우고 넘치는 부분은 잘라냄
      position: "center", // 중앙을 기준으로 크롭
    })
    .toFile(outputPath);
}

/**
 * 디렉토리 내의 모든 이미지 파일을 리사이즈하는 함수
 * @param {string} inputDir - 원본 이미지들이 있는 디렉토리 경로
 * @param {string} outputDir - 변환된 이미지들을 저장할 디렉토리 경로
 * @param {string[]} [extensions=['.jpg', '.jpeg', '.png', '.gif']] - 처리할 이미지 확장자 배열
 * @returns {Promise<void>}
 */
async function resizeImagesInDirectory(
  inputDir,
  outputDir,
  extensions = [".jpg", ".jpeg", ".png", ".gif"]
) {
  // 출력 디렉토리가 없으면 생성
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 디렉토리 내의 모든 파일 읽기
  const files = fs.readdirSync(inputDir);

  // 각 파일에 대해 처리
  for (const file of files) {
    const ext = path.extname(file).toLowerCase();

    // 지정된 확장자의 파일만 처리
    if (extensions.includes(ext)) {
      const inputPath = path.join(inputDir, file);

      try {
        // 입력 파일의 해시 계산
        const hash = await calculateFileHash(inputPath);
        const outputFileName = `${hash}${ext}`;
        const outputPath = path.join(outputDir, outputFileName);

        // 해당 해시의 파일이 이미 존재하는지 확인
        if (fs.existsSync(outputPath)) {
          console.log(`스킵: ${file} (이미 처리된 파일)`);
          continue;
        }

        // 이미지 리사이즈 처리
        await resizeImage(inputPath, outputPath);
        console.log(`성공: ${file} -> ${outputFileName}`);
      } catch (error) {
        console.error(`실패: ${file} 처리 중 오류 발생`, error);
      }
    }
  }
}

resizeImagesInDirectory("./images", "./images/resized");
