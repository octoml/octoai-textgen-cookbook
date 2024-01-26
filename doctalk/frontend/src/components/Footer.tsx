import Image from "next/image";

const Footer = () => {
  return (
    <footer>
      <div className="container">
        <nav>
          <ul>
            <li className="with-icon">
              <a
                href="https://github.com/octoml/octoai-textgen-cookbook/tree/main/doctalk/frontend"
                target="_blank"
              >
                <Image
                  src="/icons/github.svg"
                  alt="Github Icon"
                  width="18"
                  height="18"
                />
                View on Github
              </a>
            </li>
          </ul>
          <ul>
            <li className="multilink">
              <a href="https://octo.ai/?utm_source=doctalk" target="_blank">
                Powered by OctoAI
              </a>
              <a href="https://www.pinecone.io/" target="_blank">
                and Pinecone
              </a>
            </li>
            <li>
              <a
                href="https://octo.ai/legals/privacy-policy/?utm_source=doctalk"
                target="_blank"
              >
                Privacy Policy
              </a>
            </li>
            <li>
              <a
                href="https://octo.ai/legals/terms-of-use/?utm_source=doctalk"
                target="_blank"
              >
                Terms of Use
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </footer>
  );
};

export default Footer;
