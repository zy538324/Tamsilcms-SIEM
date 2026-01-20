type SectionHeaderProps = {
  title: string;
  description: string;
  actionLabel?: string;
};

const SectionHeader = ({ title, description, actionLabel }: SectionHeaderProps) => (
  <div className="section-header">
    <div>
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
    {actionLabel ? (
      <button className="ghost-button" type="button">
        {actionLabel}
      </button>
    ) : null}
  </div>
);

export default SectionHeader;
